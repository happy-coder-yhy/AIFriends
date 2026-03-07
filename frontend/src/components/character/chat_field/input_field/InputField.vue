<script setup lang="ts">
import { useTemplateRef, ref } from 'vue';
import MicrophoneIcon from '../../icons/MicrophoneIcon.vue';
import SendIcon from '../../icons/SendIcon.vue';
import streamApi from '@/ts/http/streamApi'

const props = defineProps(['friendId'])
const emit = defineEmits(['pushBackMessage', 'addToLastMessage'])
const inputRef = useTemplateRef('input-ref')
const message = ref('')
let isProcessing = false

function focus() {
    inputRef.value?.focus()
}

async function handleSend() {
    if (isProcessing) return // 正在提交中
    isProcessing = true

    const content = message.value.trim()
    if (!content) return
    message.value = ''

    emit('pushBackMessage', {role: 'user', content: content, id: crypto.randomUUID()})
    emit('pushBackMessage', {role: 'ai', content: '', id: crypto.randomUUID()})

    try {
        await streamApi('/api/friend/message/chat/', {
            body: {
                friend_id: props.friendId,
                message: content
            },
            onmessage(data: any, isDone: any) {
                if (isDone) {
                    isProcessing = false
                } else if (data.content) {
                    // console.log(data.content)
                    emit('addToLastMessage', data.content)
                }
            },
            onerror(err: any) {
                isProcessing = false
            },
        })
    } catch(err) {
        console.log(err)
        isProcessing = false
    }
}

defineExpose({
    focus,
})
</script>

<template>
    <form @submit.prevent="handleSend" class="absolute bottom-4 left-2 h-12 w-86 flex items-center">
        <input
            ref="input-ref"
            v-model="message"
            class="input w-full h-full rounded-xl pr-20 bg-black/30 backdrop-blur-sm text-white text-base focus:outline-none focus:border-none" 
            type="text" 
            placeholder="请输入消息..."
        >
        <div @click="handleSend" class="absolute right-2 w-6 h-6 flex justify-center items-center cursor-pointer">
            <SendIcon />
        </div>
        <div class="absolute right-10 w-6 h-6 flex justify-center items-center cursor-pointer">
            <MicrophoneIcon />
        </div>
    </form>

</template>

<style scoped>

</style>
