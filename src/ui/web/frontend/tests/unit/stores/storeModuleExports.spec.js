import { describe, expect, it } from 'vitest'
import * as capabilitiesFacade from '@/stores/capabilitiesStore'
import * as metadataModule from '@/stores/builder/metadata'

describe('store module exports', () => {
  it('keeps the capabilities compatibility entry point importable', () => {
    expect(Object.keys(capabilitiesFacade)).toEqual(['useCapabilitiesStore'])
    expect(capabilitiesFacade.useCapabilitiesStore).toBeTypeOf('function')
  })

  it('exports only implemented metadata factories', () => {
    expect(metadataModule.createMetadataState).toBeTypeOf('function')
    expect(metadataModule.createTemplateActions).toBeTypeOf('function')
    expect(metadataModule.createSectionActions).toBeTypeOf('function')
    expect(metadataModule.createComponentActions).toBeTypeOf('function')
    expect(metadataModule.createSaveActions).toBeTypeOf('function')
    expect(metadataModule.createMetadataGetters).toBeUndefined()
  })
})
