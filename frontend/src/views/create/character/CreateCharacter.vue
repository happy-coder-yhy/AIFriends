<script setup lang="ts">
import { ref, useTemplateRef } from 'vue';
import BackgroundImage from './components/BackgroundImage.vue';
import Name from './components/Name.vue';
import Photo from './components/Photo.vue';
import Profile from './components/Profile.vue';
import { base64ToFile } from '@/ts/utils/base64_to_file';
import api from '@/ts/http/api';
import { useRouter } from 'vue-router';
import { useUserStore } from '@/stores/user';

const user = useUserStore()
const router = useRouter()

const photoRef = useTemplateRef('photo-ref')
const nameRef = useTemplateRef('name-ref')
const profileRef = useTemplateRef('profile-ref')
const backgroundImageRef = useTemplateRef('background-image-ref')
const errorMessage = ref('')

async function handleCreate() {
    const photo = photoRef.value?.myPhoto
    const name = nameRef.value?.myName?.trim()
    const profile = profileRef.value?.myProfile?.trim()
    const backgroundImage = backgroundImageRef.value?.myBackgroundImage

    if (!photo) {
        errorMessage.value = '头像不能为空！'
    } else if (!name) {
        errorMessage.value = '名称不能为空！'
    } else if (!profile) {
        errorMessage.value = '角色介绍不能为空！'
    } else if (!backgroundImage) {
        errorMessage.value = '聊天背景不能为空！'
    } else {
        const formData = new FormData()
        formData.append('name', name)
        formData.append('profile', profile)
        formData.append('photo', base64ToFile(photo, 'photo.png'))
        formData.append('background_image', base64ToFile(backgroundImage, 'background_image.png'))

        try {
            const res = await api.post('/api/create/character/create/', formData)
            const data = res.data
            if (data.result === 'success') {
                await router.push({
                    name: 'user-space-index',
                    params: {
                        user_id: user.id,
                    }
                })
            } else {
                errorMessage.value = data.result
            }

        } catch (err) {
            console.log(err)
        }
    }
}
</script>

<template>
    <div class="flex justify-center">
        <div class="card w-120 bg-blue-300 shadow-sm mt-10">
            <div class="card-body">
                <h3 class="text-lg font-bold">创建角色</h3>
                <Photo ref="photo-ref" />
                <Name ref="name-ref" />
                <Profile ref="profile-ref" />
                <BackgroundImage ref="background-image-ref" />

                <p v-if="errorMessage" class="text-sm text-red-500 font-bold">{{ errorMessage }}</p>

                <div class="flex justify-center">
                    <button @click="handleCreate" class="btn btn-primary w-60 mt-2">创建</button>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>

</style>
