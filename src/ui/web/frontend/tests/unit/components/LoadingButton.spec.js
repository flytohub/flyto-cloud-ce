import { describe, expect, it } from 'vitest'
import { shallowMount } from '@vue/test-utils'

import LoadingButton from '@/components/common/LoadingButton.vue'

describe('LoadingButton.vue', () => {
  it.each(['sm', 'md', 'lg'])('uses a collision-free class for the %s size', (size) => {
    const wrapper = shallowMount(LoadingButton, {
      props: { size },
      slots: { default: 'Run' },
    })

    expect(wrapper.classes()).toContain(`loading-button--${size}`)
    expect(wrapper.classes()).not.toContain(`size-${size}`)
  })

  it('preserves the public click behavior', async () => {
    const wrapper = shallowMount(LoadingButton, {
      slots: { default: 'Run' },
    })

    await wrapper.trigger('click')

    expect(wrapper.emitted('click')).toHaveLength(1)
  })
})
