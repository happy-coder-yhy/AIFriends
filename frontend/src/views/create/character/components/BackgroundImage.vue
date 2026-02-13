<script setup lang="ts">
import CameraIcon from '@/views/user/profile/components/icon/CameraIcon.vue'
import { ref, watch, onBeforeUnmount, useTemplateRef, nextTick } from 'vue'
import Croppie from 'croppie'
import 'croppie/croppie.css'

const props = defineProps(['backgroundImage'])
const myBackgroundImage = ref(props.backgroundImage)

watch(() => props.backgroundImage, newVal => {
    myBackgroundImage.value = newVal
})

const fileInputRef = useTemplateRef('file-input-ref')
const modalRef = useTemplateRef('modal-ref')
const croppieRef = useTemplateRef('croppie-ref')
let croppie:any = null

async function openModal(photo:any) {
    modalRef.value?.showModal()
    await nextTick()

    if (!croppie) {
        croppie = new (Croppie as any)(croppieRef.value, {
            viewport: {width: 300, height: 500},
            boundary: {width: 600, height: 600},
            enableOrientation: true,
            enforceBoundary: true,
        })
    }

    croppie.bind({
        url: photo,
    })
}

async function crop() {
    if (!croppie) return

    myBackgroundImage.value = await croppie.result({
        type: 'base64',
        size: 'viewport',
    })

    modalRef.value?.close()
}

function onFileChange(e:any) {
    const file = e.target.files[0]
    e.target.value = ''
    
    if (!file) return 
    
    const reader = new FileReader()
    reader.onload = () => {
        openModal(reader.result)
    }
    reader.readAsDataURL(file)
}

onBeforeUnmount(() => {
    croppie?.destroy()
})

defineExpose({
    myBackgroundImage,
})
</script>

<template>
    <fieldset class="fieldset">
        <label class="label text-base italic">聊天背景</label>
        <div class="avatar relative">
            <div v-if="myBackgroundImage" class="w-15 h-25 rounded-box">
                <img :src="myBackgroundImage" alt="">
            </div>

            <div v-else class="w-15 h-25 rounded-box bg-blue-500"></div>
            <div @click="fileInputRef?.click()" class="w-15 h-25 rounded-box absolute top-0 left-0 bg-black/20 flex justify-center items-center cursor-pointer">
                <CameraIcon />
            </div>
        </div>
    </fieldset>

    <input ref="file-input-ref" type="file" class="hidden" accept="image/*" @change="onFileChange">

    <dialog ref="modal-ref" class="modal">
        <div class="modal-box transition-none max-w-2xl">
            <button @click="modalRef?.close()" class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2">✕</button>

            <div ref="croppie-ref" class="flex flex-col my-4"></div>

            <div class="modal-action flex">
                <button @click="modalRef?.close()" class="btn btn-outline btn-error w-20 h-10">取消</button>
                <button @click="crop" class="btn btn-outline btn-primary w-20 h-10">确定</button>
            </div>
        </div>
    </dialog>
</template>

<style scoped>

</style>
