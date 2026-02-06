<script setup lang="ts">
import { ref, watch } from 'vue'

const props = defineProps(['name'])
const myName = ref(props.name)

watch(() => props.name, newVal => {
    myName.value = newVal
})

defineExpose({
    myName,
})
</script>

<template>
    <fieldset class="fieldset">
        <label class="label text-base italic">名称</label>
        <input v-model="myName" type="text" class="input w-108 focus:outline-none focus:border-blue-500">
    </fieldset>
</template>

<style scoped>

</style>
