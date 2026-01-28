<script setup lang="ts">
import { useUserStore } from "@/stores/user"

const user = useUserStore()

</script>

<template>
个人: {{ user.username }}
</template>

<style scoped>

</style>