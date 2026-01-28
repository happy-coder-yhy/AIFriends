<script setup lang="ts">
import { useRoute } from 'vue-router';


const route = useRoute(); // 获取路由参数

</script>

<template>
个人空间: {{ route.params.user_id }}
</template>

<style scoped>

</style>