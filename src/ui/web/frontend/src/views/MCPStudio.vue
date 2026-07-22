<template>
  <main class="mcp-studio dark">
    <WaveHero size="small" variant="purple" wave-height="32px">
      <div class="studio-hero-copy">
        <div class="studio-heading">
          <div class="studio-kicker"><Blocks :size="16" /> {{ t('mcpStudio.kicker') }}</div>
          <div class="studio-title-line">
            <h1>{{ t('mcpStudio.title') }}</h1>
            <StatusBadge
              :status="status.ok ? 'success' : 'error'"
              :label="status.ok ? t('mcpStudio.status.online') : t('mcpStudio.status.offline')"
              size="md"
              show-icon
            />
          </div>
          <p>{{ t('mcpStudio.summary', { transport: status.transport, count: status.exposedToolCount, access: accessLabel }) }}</p>
        </div>
        <div class="studio-actions">
          <LoadingButton
            variant="outline"
            size="sm"
            :icon="RefreshCw"
            :loading="loading"
            :loading-text="t('mcpStudio.actions.refreshing')"
            :disabled="loading"
            @click="loadStatus"
          >
            {{ t('mcpStudio.actions.refresh') }}
          </LoadingButton>
          <LoadingButton
            :icon="Plus"
            :loading="creating"
            :loading-text="t('mcpStudio.actions.creating')"
            @click="createTool"
          >
            {{ t('mcpStudio.actions.newTool') }}
          </LoadingButton>
        </div>
      </div>
    </WaveHero>

    <div class="studio-content">

    <div v-if="error" class="error-banner" role="alert">
      <AlertTriangle :size="17" />
      <span>{{ error }}</span>
      <button type="button" @click="loadStatus">{{ t('mcpStudio.actions.retry') }}</button>
    </div>

    <section class="server-bar" :aria-label="t('mcpStudio.server.aria')">
      <div class="server-identity">
        <Server :size="18" />
        <div>
          <strong>{{ status.title }}</strong>
          <span>{{ status.name }}</span>
        </div>
      </div>
      <div class="endpoint-value">
        <span>{{ t('mcpStudio.server.endpoint') }}</span>
        <code>{{ status.serverUrl }}</code>
        <button class="inline-icon" type="button" :title="t('mcpStudio.server.copyEndpoint')" @click="copyText(status.serverUrl, 'endpoint')">
          <Check v-if="copied === 'endpoint'" :size="15" />
          <Copy v-else :size="15" />
          <span class="sr-only">{{ t('mcpStudio.server.copyEndpoint') }}</span>
        </button>
      </div>
      <div class="protocol-value">
        <span>{{ t('mcpStudio.server.protocol') }}</span>
        <strong>{{ latestProtocol }}</strong>
      </div>
    </section>

    <nav class="studio-tabs" :aria-label="t('mcpStudio.tabs.aria')">
      <PageTabs v-model="activeTab" :tabs="studioTabs" />
    </nav>

    <section v-if="activeTab === 'tools'" class="tools-layout">
      <aside class="tool-index" :aria-label="t('mcpStudio.tools.toolListAria')">
        <label class="search-field">
          <Search :size="16" />
          <AppInput v-model="search" type="search" size="sm" :placeholder="t('mcpStudio.tools.searchPlaceholder')" />
        </label>
        <div class="tool-list">
          <button
            v-for="tool in visibleTools"
            :key="tool.name"
            class="tool-list-item"
            :class="{ selected: selectedTool?.name === tool.name }"
            type="button"
            @click="selectTool(tool)"
          >
            <span class="tool-icon"><Workflow :size="16" /></span>
            <span class="tool-copy">
              <strong>{{ tool.name }}</strong>
              <small>{{ tool.description || t('mcpStudio.tools.defaultDescription') }}</small>
            </span>
            <ChevronRight :size="16" />
          </button>
          <div v-if="!visibleTools.length" class="tool-empty">
            <SearchX v-if="search" :size="22" />
            <Blocks v-else :size="22" />
            <span>{{ search ? t('mcpStudio.tools.noMatches') : t('mcpStudio.tools.noneYet') }}</span>
          </div>
        </div>
      </aside>

      <div v-if="selectedTool" class="tool-workbench">
        <div class="tool-header">
          <div>
            <div class="tool-name-line">
              <h2>{{ selectedTool.name }}</h2>
              <span>{{ t('mcpStudio.tools.inputCount', { count: selectedFields.length }) }}</span>
            </div>
            <p>{{ selectedTool.description || t('mcpStudio.tools.technicalDescription') }}</p>
          </div>
          <LoadingButton
            v-if="selectedSource.id"
            variant="outline"
            size="sm"
            :icon="Pencil"
            @click="router.push(`/templates/builder/${selectedSource.id}`)"
          >
            {{ t('mcpStudio.actions.editWorkflow') }}
          </LoadingButton>
        </div>

        <div class="workbench-body">
          <form class="argument-form" @submit.prevent="runSelected">
            <div class="section-heading">
              <div>
                <h3>{{ t('mcpStudio.tools.arguments') }}</h3>
                <span>{{ t('mcpStudio.tools.schema') }}</span>
              </div>
              <button class="text-button" type="button" @click="resetArguments">{{ t('mcpStudio.actions.reset') }}</button>
            </div>

            <div v-if="selectedFields.length" class="field-grid">
              <div v-for="field in selectedFields" :key="field.name" class="argument-field">
                <span class="field-label">
                  <code>{{ field.name }}</code>
                  <em>{{ field.type }}</em>
                  <b v-if="field.required">{{ t('mcpStudio.tools.required') }}</b>
                </span>
                <AppSelect
                  v-if="field.enumValues.length"
                  v-model="argumentValues[field.name]"
                  :options="field.enumValues"
                  :aria-label="field.name"
                  :placeholder="t('mcpStudio.tools.selectValue')"
                  size="sm"
                />
                <label v-else-if="field.type === 'boolean'" class="boolean-control">
                  <input v-model="argumentValues[field.name]" :aria-label="field.name" type="checkbox" />
                  <span>{{ argumentValues[field.name] ? t('mcpStudio.tools.booleanTrue') : t('mcpStudio.tools.booleanFalse') }}</span>
                </label>
                <AppTextarea
                  v-else-if="field.type === 'object' || field.type === 'array'"
                  v-model="argumentValues[field.name]"
                  :aria-label="field.name"
                  rows="5"
                  spellcheck="false"
                />
                <AppInput
                  v-else
                  v-model="argumentValues[field.name]"
                  :aria-label="field.name"
                  :type="field.type === 'number' || field.type === 'integer' ? 'number' : 'text'"
                  :step="field.type === 'integer' ? '1' : 'any'"
                  size="sm"
                />
                <small v-if="field.description">{{ field.description }}</small>
              </div>
            </div>
            <div v-else class="no-arguments">
              <Braces :size="20" />
              <span>{{ t('mcpStudio.tools.noArguments') }}</span>
            </div>

            <div v-if="runError" class="field-error" role="alert">{{ runError }}</div>
            <LoadingButton
              class="run-action"
              type="submit"
              :icon="Play"
              :loading="running"
              :loading-text="t('mcpStudio.actions.running')"
            >
              {{ t('mcpStudio.actions.runTool') }}
            </LoadingButton>
          </form>

          <section class="result-panel" aria-live="polite">
            <div class="section-heading">
              <div>
                <h3>{{ t('mcpStudio.tools.response') }}</h3>
                <span>{{ responseStateLabel }}</span>
              </div>
              <button
                v-if="formattedResponse"
                class="inline-icon"
                type="button"
                :title="t('mcpStudio.tools.copyResponse')"
                @click="copyText(formattedResponse, 'response')"
              >
                <Check v-if="copied === 'response'" :size="15" />
                <Copy v-else :size="15" />
                <span class="sr-only">{{ t('mcpStudio.tools.copyResponse') }}</span>
              </button>
            </div>
            <pre v-if="formattedResponse">{{ formattedResponse }}</pre>
            <div v-else class="response-empty">
              <SquareTerminal :size="23" />
              <span>{{ t('mcpStudio.tools.output') }}</span>
            </div>
          </section>
        </div>
      </div>

      <div v-else class="workbench-empty">
        <Blocks :size="28" />
        <strong>{{ search ? t('mcpStudio.tools.noSelection') : t('mcpStudio.actions.createFirst') }}</strong>
        <LoadingButton v-if="!search" :icon="Plus" @click="createTool">
          {{ t('mcpStudio.actions.newTool') }}
        </LoadingButton>
      </div>
    </section>

    <section v-else-if="activeTab === 'connect'" class="connect-layout">
      <div class="client-selector">
        <button
          v-for="client in clients"
          :key="client.id"
          type="button"
          :class="{ active: selectedClientId === client.id }"
          @click="selectedClientId = client.id"
        >
          <TerminalSquare :size="18" />
          <span>{{ client.label }}</span>
          <small>{{ client.format }}</small>
        </button>
      </div>
      <div class="config-panel">
        <div class="section-heading">
          <div>
            <h2>{{ selectedClient.label }}</h2>
            <span>{{ selectedClient.format }}</span>
          </div>
          <LoadingButton
            variant="outline"
            size="sm"
            :icon="copied === 'config' ? Check : Copy"
            @click="copyText(selectedClient.content, 'config')"
          >
            {{ copied === 'config' ? t('mcpStudio.actions.copied') : t('mcpStudio.actions.copy') }}
          </LoadingButton>
        </div>
        <pre>{{ selectedClient.content }}</pre>
      </div>
    </section>

    <section v-else class="audit-layout">
      <div class="audit-checks">
        <div v-for="checkItem in checks" :key="checkItem.id" class="audit-row">
          <span :class="checkItem.pass ? 'audit-pass' : 'audit-fail'">
            <CheckCircle2 v-if="checkItem.pass" :size="17" />
            <XCircle v-else :size="17" />
          </span>
          <strong>{{ checkItem.label }}</strong>
          <small>{{ checkItem.pass ? t('mcpStudio.audit.pass') : t('mcpStudio.audit.review') }}</small>
        </div>
      </div>
      <div class="protocol-panel">
        <div class="section-heading">
          <div>
            <h2>{{ t('mcpStudio.audit.protocolSurface') }}</h2>
            <span>{{ t('mcpStudio.audit.versionCount', { count: status.protocolVersions.length }) }}</span>
          </div>
          <ShieldCheck :size="20" />
        </div>
        <dl>
          <div><dt>{{ t('mcpStudio.audit.transport') }}</dt><dd>{{ status.transport }}</dd></div>
          <div><dt>{{ t('mcpStudio.audit.access') }}</dt><dd>{{ accessLabel }}</dd></div>
          <div><dt>{{ t('mcpStudio.audit.toolsChanged') }}</dt><dd>{{ status.capabilities?.tools?.listChanged ? t('mcpStudio.audit.notified') : t('mcpStudio.audit.static') }}</dd></div>
          <div><dt>{{ t('mcpStudio.audit.evidence') }}</dt><dd>{{ evidenceCount }}</dd></div>
        </dl>
      </div>
      <div class="history-panel">
        <div class="section-heading">
          <div>
            <h2>{{ t('mcpStudio.audit.sessionHistory') }}</h2>
            <span>{{ t('mcpStudio.audit.callCount', { count: history.length }) }}</span>
          </div>
          <button v-if="history.length" class="text-button" type="button" @click="history = []">{{ t('mcpStudio.actions.clear') }}</button>
        </div>
        <div v-if="history.length" class="history-list">
          <button
            v-for="entry in history"
            :key="entry.id"
            type="button"
            @click="restoreHistory(entry)"
          >
            <span :class="entry.ok ? 'history-pass' : 'history-fail'" />
            <strong>{{ entry.tool }}</strong>
            <small>{{ entry.duration }} ms</small>
          </button>
        </div>
        <div v-else class="history-empty">{{ t('mcpStudio.audit.noCalls') }}</div>
      </div>
    </section>
    </div>
  </main>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'
import {
  AlertTriangle,
  Blocks,
  Braces,
  Check,
  CheckCircle2,
  ChevronRight,
  Copy,
  FileCheck2,
  Pencil,
  Play,
  PlugZap,
  Plus,
  RefreshCw,
  Search,
  SearchX,
  Server,
  ShieldCheck,
  SquareTerminal,
  TerminalSquare,
  Workflow,
  Wrench,
  XCircle,
} from 'lucide-vue-next'
import { callMcpTool, getMcpStatus } from '@/api/mcp'
import { templatesAPI } from '@/api/templates'
import AppInput from '@/components/common/AppInput.vue'
import AppSelect from '@/components/common/AppSelect.vue'
import AppTextarea from '@/components/common/AppTextarea.vue'
import LoadingButton from '@/components/common/LoadingButton.vue'
import PageTabs from '@/components/common/PageTabs.vue'
import StatusBadge from '@/components/common/StatusBadge.vue'
import WaveHero from '@/components/common/WaveHero.vue'
import {
  auditChecks,
  clientConfigurations,
  createMcpStarter,
  initialArguments,
  normalizeMcpStatus,
  parseArguments,
  schemaFields,
  toolSource,
} from '@/features/mcp/studioModel'

const router = useRouter()
const { t } = useI18n()
const loading = ref(false)
const creating = ref(false)
const running = ref(false)
const error = ref('')
const runError = ref('')
const status = ref(normalizeMcpStatus({}))
const activeTab = ref('tools')
const search = ref('')
const selectedToolName = ref('')
const selectedClientId = ref('codex')
const argumentValues = ref({})
const response = ref(null)
const responseState = ref('ready')
const copied = ref('')
const history = ref([])

const tabs = [
  { id: 'tools', labelKey: 'mcpStudio.tabs.tools', icon: Wrench },
  { id: 'connect', labelKey: 'mcpStudio.tabs.connect', icon: PlugZap },
  { id: 'audit', labelKey: 'mcpStudio.tabs.audit', icon: FileCheck2 },
]
const studioTabs = computed(() => tabs.map(tab => ({
  ...tab,
  label: t(tab.labelKey),
  count: tab.id === 'tools' ? status.value.exposedToolCount : undefined,
})))

const visibleTools = computed(() => {
  const needle = search.value.trim().toLowerCase()
  if (!needle) return status.value.tools
  return status.value.tools.filter(tool => (
    `${tool.name} ${tool.description || ''}`.toLowerCase().includes(needle)
  ))
})
const selectedTool = computed(() => (
  status.value.tools.find(tool => tool.name === selectedToolName.value) || null
))
const selectedFields = computed(() => schemaFields(selectedTool.value))
const selectedSource = computed(() => toolSource(selectedTool.value))
const clients = computed(() => clientConfigurations(status.value).map(client => ({
  ...client,
  label: client.id === 'desktop' || client.id === 'http'
    ? t(`mcpStudio.clients.${client.id}`)
    : client.label,
})))
const selectedClient = computed(() => (
  clients.value.find(client => client.id === selectedClientId.value) || clients.value[0]
))
const checks = computed(() => auditChecks(status.value).map(checkItem => {
  const labelKey = checkItem.id === 'access'
    ? (status.value.auth.localLoopbackAccountless ? 'mcpStudio.checks.accessLocal' : 'mcpStudio.checks.accessBearer')
    : `mcpStudio.checks.${checkItem.id}`
  return { ...checkItem, label: t(labelKey) }
}))
const latestProtocol = computed(() => status.value.protocolVersions[0] || 'MCP')
const accessLabel = computed(() => {
  if (status.value.auth.localLoopbackAccountless) return t('mcpStudio.access.localAccountless')
  if (status.value.auth.configured) return t('mcpStudio.access.bearerConnected')
  return status.value.auth.required ? t('mcpStudio.access.bearerRequired') : t('mcpStudio.access.operator')
})
const responseStateLabel = computed(() => t(`mcpStudio.tools.${responseState.value}`))
const formattedResponse = computed(() => {
  if (!response.value) return ''
  return JSON.stringify(response.value, null, 2)
})
const evidenceCount = computed(() => (
  (Array.isArray(status.value.evidence) ? status.value.evidence.length : 0) +
  (Array.isArray(status.value.recentExecutions) ? status.value.recentExecutions.length : 0)
))

function selectTool(tool) {
  selectedToolName.value = tool.name
  resetArguments()
  response.value = null
  responseState.value = 'ready'
  runError.value = ''
}

function resetArguments() {
  argumentValues.value = initialArguments(selectedTool.value)
  runError.value = ''
}

async function loadStatus() {
  loading.value = true
  error.value = ''
  const result = await getMcpStatus()
  status.value = normalizeMcpStatus(result)
  loading.value = false
  if (!status.value.ok) error.value = result.error || t('mcpStudio.errors.statusUnavailable')
  if (!selectedTool.value && status.value.tools.length) selectTool(status.value.tools[0])
}

async function createTool() {
  if (creating.value) return
  creating.value = true
  error.value = ''
  const result = await templatesAPI.createTemplate(createMcpStarter(status.value.exposedToolCount + 1))
  creating.value = false
  if (!result.ok) {
    error.value = result.error || t('mcpStudio.errors.createFailed')
    return
  }
  router.push(`/templates/builder/${result.template.id}`)
}

async function runSelected() {
  if (!selectedTool.value || running.value) return
  runError.value = ''
  let args
  try {
    args = parseArguments(selectedTool.value, argumentValues.value)
  } catch (validationError) {
    runError.value = validationError.message
    return
  }

  running.value = true
  responseState.value = 'running'
  const startedAt = performance.now()
  const result = await callMcpTool(selectedTool.value.name, args)
  const duration = Math.round(performance.now() - startedAt)
  running.value = false
  response.value = result.response || { error: result.error }
  responseState.value = result.ok ? 'completed' : 'failed'
  if (!result.ok) runError.value = result.error || t('mcpStudio.errors.callFailed')
  history.value = [{
    id: `${Date.now()}-${selectedTool.value.name}`,
    tool: selectedTool.value.name,
    args,
    response: response.value,
    ok: result.ok,
    duration,
  }, ...history.value].slice(0, 20)
}

function restoreHistory(entry) {
  const tool = status.value.tools.find(item => item.name === entry.tool)
  if (tool) {
    activeTab.value = 'tools'
    selectedToolName.value = tool.name
    argumentValues.value = { ...initialArguments(tool), ...entry.args }
    response.value = entry.response
    responseState.value = entry.ok ? 'completed' : 'failed'
  }
}

async function copyText(value, key) {
  if (!value || typeof navigator === 'undefined' || !navigator.clipboard) return
  await navigator.clipboard.writeText(String(value))
  copied.value = key
  window.setTimeout(() => { if (copied.value === key) copied.value = '' }, 1600)
}

onMounted(loadStatus)
</script>

<style scoped src="../features/mcp/studio.css"></style>
