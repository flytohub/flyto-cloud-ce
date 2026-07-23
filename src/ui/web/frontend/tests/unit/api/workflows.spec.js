import { describe, it, expect, vi, beforeEach } from 'vitest'

vi.mock('@/api/client', () => ({
  post: vi.fn()
}))

vi.mock('@/api/config', () => ({
  API_ENDPOINTS: {
    WORKFLOWS: {
      RUN: '/workflows/run'
    }
  }
}))

import { post } from '@/api/client'
import { workflowAPI } from '@/api/workflows'

describe('Workflows API', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  // =========================================================================
  // run
  // =========================================================================

  describe('run()', () => {
    it('calls POST /workflows/run with YAML and params', async () => {
      post.mockResolvedValue({ ok: true, executionId: 'exec-2' })

      const yaml = 'steps:\n  - module: browser.goto'
      await workflowAPI.run(yaml, { url: 'https://test.com' })

      expect(post).toHaveBeenCalledWith('/workflows/run', {
        workflowYaml: yaml,
        params: { url: 'https://test.com' }
      })
    })

    it('includes startStep and endStep when provided', async () => {
      post.mockResolvedValue({ ok: true })

      await workflowAPI.run('yaml', {}, { startStep: 1, endStep: 3 })

      expect(post).toHaveBeenCalledWith('/workflows/run', {
        workflowYaml: 'yaml',
        params: {},
        startStep: 1,
        endStep: 3
      })
    })

    it('includes breakpoints when provided', async () => {
      post.mockResolvedValue({ ok: true })

      await workflowAPI.run('yaml', {}, { breakpoints: ['node_1', 'node_2'] })

      expect(post).toHaveBeenCalledWith('/workflows/run', {
        workflowYaml: 'yaml',
        params: {},
        breakpoints: ['node_1', 'node_2']
      })
    })

    it('does not include breakpoints when array is empty', async () => {
      post.mockResolvedValue({ ok: true })

      await workflowAPI.run('yaml', {}, { breakpoints: [] })

      const payload = post.mock.calls[0][1]
      expect(payload.breakpoints).toBeUndefined()
    })

    it('includes screenshotMode when provided', async () => {
      post.mockResolvedValue({ ok: true })

      await workflowAPI.run('yaml', {}, { screenshotMode: 'all' })

      expect(post).toHaveBeenCalledWith('/workflows/run', {
        workflowYaml: 'yaml',
        params: {},
        screenshotMode: 'all'
      })
    })
  })

  // =========================================================================
  // stepsToVueFlow / vueFlowToSteps
  // =========================================================================

  describe('stepsToVueFlow()', () => {
    it('calls POST /workflows/steps-to-vueflow', async () => {
      post.mockResolvedValue({ ok: true, nodes: [], edges: [] })

      await workflowAPI.stepsToVueFlow({ steps: [{ module: 'a' }] })

      expect(post).toHaveBeenCalledWith('/workflows/steps-to-vueflow', { steps: [{ module: 'a' }] })
    })
  })

  describe('vueFlowToSteps()', () => {
    it('calls POST /workflows/vueflow-to-steps', async () => {
      post.mockResolvedValue({ ok: true, steps: [] })

      await workflowAPI.vueFlowToSteps({ nodes: [], edges: [] })

      expect(post).toHaveBeenCalledWith('/workflows/vueflow-to-steps', { nodes: [], edges: [] })
    })
  })

  // =========================================================================
  // validate
  // =========================================================================

  describe('validate()', () => {
    it('calls POST /workflows/validate', async () => {
      post.mockResolvedValue({ valid: true, errors: [], warnings: [] })

      const result = await workflowAPI.validate({ steps: [] })

      expect(post).toHaveBeenCalledWith('/workflows/validate', { steps: [] })
      expect(result.valid).toBe(true)
    })
  })

  // =========================================================================
  // computeLayout / computeGraphRelations
  // =========================================================================

  describe('computeLayout()', () => {
    it('calls POST /workflows/layout', async () => {
      post.mockResolvedValue({ ok: true, positions: {} })

      await workflowAPI.computeLayout({ nodes: [], edges: [] })

      expect(post).toHaveBeenCalledWith('/workflows/layout', { nodes: [], edges: [] })
    })
  })

  describe('computeGraphRelations()', () => {
    it('calls POST /workflows/graph-relations', async () => {
      post.mockResolvedValue({ ok: true, relations: {} })

      await workflowAPI.computeGraphRelations({ nodes: [], edges: [] })

      expect(post).toHaveBeenCalledWith('/workflows/graph-relations', { nodes: [], edges: [] })
    })
  })
})
