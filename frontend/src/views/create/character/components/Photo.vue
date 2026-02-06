<script setup lang="ts">
import { onBeforeUnmount, ref, useTemplateRef, watch } from 'vue';
import Croppie from 'croppie'
import 'croppie/croppie.css'
import CameraIcon from '@/views/user/profile/components/icon/CameraIcon.vue';

const props = defineProps(['photo'])
const myPhoto = ref(props.photo)

// 监听
watch(() => props.photo, newValue => {
  myPhoto.value = newValue
})

const fileInputRef = useTemplateRef('file-input-ref')
const modalRef = useTemplateRef('modal-ref')
const croppieRef = useTemplateRef('croppie-ref')
let croppie:any = null

async function openModal(photo:any) {
    modalRef.value?.showModal()

    if (!croppie) {
        croppie = new (Croppie as any)(croppieRef.value, {
            viewport: {width: 200, height: 200, type: 'square'},
            boundary: {width: 300, height: 300},
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

    myPhoto.value = await croppie.result({
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

// 暴露
defineExpose({
  myPhoto
})
</script>

<template>
    <div class="flex justify-center">
        <div class="avatar relative">
            <div v-if="myPhoto" class="w-28 rounded-full">
                <img :src="myPhoto" alt="">
            </div>
            <div v-else class="w-28 h-28 rounded-full bg-blue-500"></div>
            <div @click="fileInputRef?.click()" class="w-28 h-28 rounded-full bg-black/20 absolute left-0 top-0 flex justify-center items-center cursor-pointer">
                <CameraIcon />
            </div>
        </div>
    </div>

    <input ref="file-input-ref" type="file" class="hidden" accept="image/*" @change="onFileChange">

    <dialog ref="modal-ref" class="modal">
        <div class="modal-box transition-none">
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
