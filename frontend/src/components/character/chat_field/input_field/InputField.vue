<script setup lang="ts">
import MicrophoneIcon from '../../icons/MicrophoneIcon.vue';
import SendIcon from '../../icons/SendIcon.vue';


</script>

<template>
    <div class="absolute bottom-4 left-2 h-12 w-86 flex items-center">
        <input 
            class="input w-full h-full rounded-xl pr-20 bg-black/30 backdrop-blur-sm text-white text-base focus:outline-none focus:border-none" 
            type="text" 
            placeholder="请输入消息..."
        >
        <div class="absolute right-2 w-6 h-6 flex justify-center items-center cursor-pointer">
            <SendIcon />
        </div>
        <div class="absolute right-10 w-6 h-6 flex justify-center items-center cursor-pointer">
            <MicrophoneIcon />
        </div>
    </div>

</template>

<style scoped>

</style>
