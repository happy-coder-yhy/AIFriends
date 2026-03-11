<script setup lang="ts">
import { useTemplateRef, computed, nextTick, ref } from 'vue';
import InputField from './input_field/InputField.vue';
import CharacterPhotoField from './character_photo_field/CharacterPhotoField.vue';
import ChatHistory from './chat_history/ChatHistory.vue';

const props = defineProps(['friend'])

const  modalRef = useTemplateRef('modal-ref')
const inputRef = useTemplateRef('input-ref')
const history: any = ref([])
const chatHistoryRef: any = useTemplateRef('chat-history-ref')

async function showModal() {
    modalRef.value?.showModal()
    await nextTick()
    inputRef.value?.focus()
}

const modalStyle = computed(() => {
  if (props.friend) {
    return {
      backgroundImage: `url(${props.friend.character.background_image})`,
      backgroundSize: 'cover',
      backgroundPosition: 'center',
      backgroundRepeat: 'no-repeat',
    }
  } else {
    return {}
  }
})

function handlePushBackMessage(msg: any) {
  history.value.push(msg)
  chatHistoryRef.value.scrollToBottom()
}

function handleAddToLastMessage(delta: any) {
  history.value.at(-1).content += delta
  chatHistoryRef.value.scrollToBottom()
}

function handlePushFrontMessage(msg: any) {
  history.value.unshift(msg)
}

function handleClose() {
  modalRef.value?.close()
  inputRef.value?.close()
}

defineExpose({
    showModal
})
</script>

<template>
    <dialog ref="modal-ref" class="modal">
        <div class="modal-box w-92 h-150" :style="modalStyle">
            <button @click="handleClose" class="btn btn-xs btn-circle btn-ghost bg-red-500 absolute top-3 right-2">✕</button>
            <ChatHistory
              ref="chat-history-ref"
              v-if="friend"
              :history="history"
              :friendId="friend.id"
              :character="friend.character"
              @pushFrontMessage="handlePushFrontMessage"
            />
            <InputField
              v-if="friend"
              ref="input-ref"
              :friendId="friend.id"
              @pushBackMessage="handlePushBackMessage"
              @addToLastMessage="handleAddToLastMessage"
            />
            <CharacterPhotoField v-if="friend" :character="friend.character"/>
        </div>
    </dialog>

</template>

<style scoped>

</style>
