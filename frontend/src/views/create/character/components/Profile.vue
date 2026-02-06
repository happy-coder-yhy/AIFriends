<script setup lang="ts">
import { ref, watch } from 'vue'

const props = defineProps(['profile'])
const myProfile = ref(props.profile)

watch(() => props.profile, newVal => {
    myProfile.value = newVal
})

defineExpose({
    myProfile,
})
</script>

<template>
    <fieldset class="fieldset">
        <label class="label text-base italic">角色介绍</label>
        <textarea v-model="myProfile" type="textarea" class="textarea w-108 focus:outline-none focus:border-blue-500 resize-none" rows="3"></textarea>
    </fieldset>
</template>

<style scoped>

</style>
