<script setup lang="ts">
import { useTemplateRef, ref } from 'vue';
import MicrophoneIcon from '../../icons/MicrophoneIcon.vue';
import SendIcon from '../../icons/SendIcon.vue';
import streamApi from '@/ts/http/streamApi'
import Microphone from './Microphone.vue';

const props = defineProps(['friendId'])
const emit = defineEmits(['pushBackMessage', 'addToLastMessage'])
const inputRef = useTemplateRef('input-ref')
const message = ref('')
let processId = 0
const showMic = ref(false)

function focus() {
    inputRef.value?.focus()
}

async function handleSend(event: any, audio_msg?: any) {
    let content
    if (audio_msg) {
        content = audio_msg.trim()
    } else {
        content = message.value.trim()
    }
    
    if (!content) return

    const curId = ++processId
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
                if (curId !== processId) return

                if (data.content) {
                    // console.log(data.content)
                    emit('addToLastMessage', data.content)
                }
            },
            onerror(err: any) {
      
            },
        })
    } catch(err) {
        
    }
}

function close() {
    ++processId
    showMic.value = false
}

function handleStop() {
    ++ processId
}

defineExpose({
    focus,
    close,
})
</script>

<template>
    <form v-if="!showMic" @submit.prevent="handleSend" class="absolute bottom-4 left-2 h-12 w-86 flex items-center">
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
        <div @click="showMic = true" class="absolute right-10 w-6 h-6 flex justify-center items-center cursor-pointer">
            <MicrophoneIcon />
        </div>
    </form>
    <Microphone 
        v-else
        @close="showMic = false"
        @send="handleSend"
        @stop="handleStop"
    />
</template>

<style scoped>

</style>
