<script setup lang="ts">
import { useUserStore } from "@/stores/user"
import Photo from "./components/Photo.vue";
import Username from "./components/Username.vue";
import Profile from "./components/Profile.vue";
import { ref, useTemplateRef } from "vue";
import { base64ToFile } from "@/ts/utils/base64_to_file";
import api from "@/ts/http/api";

const user = useUserStore()

const photoRef = useTemplateRef('photo-ref')
const usernameRef = useTemplateRef('username-ref')
const profileRef = useTemplateRef('profile-ref')

const errorMessage = ref('')
const showSuccessMessage = ref(false)

async function handleUpdate() {
    const photo = photoRef.value?.myPhoto
    const username = usernameRef.value?.myUsername.trim()
    const profile = profileRef.value?.myProfile.trim()

    errorMessage.value = ''
    if (!photo) {
        errorMessage.value = '头像不能为空!'   
    } else if (!username) {
        errorMessage.value = '用户名不能为空!'
    } else if (!profile) {
        errorMessage.value = '简介不能为空!'
    } else {
        const formData = new FormData()
        formData.append('username', username)
        formData.append('profile', profile)
        if (photo !== user.photo) {
            formData.append('photo', base64ToFile(photo, 'photo.png'))
        }
        try {
            const res = await api.post('/api/user/profile/update/', formData)
            const data = res.data
            if (data.result === 'success') {
                user.setUserInfo(data)
                showSuccessMessage.value = true
                setTimeout(() => {
                    showSuccessMessage.value = false
                }, 2000)
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
    <div class="relative">
        <!-- 成功提示 -->
        <div v-if="showSuccessMessage" class="absolute left-1/2 -translate-x-1/2 w-80 h-8 z-100 mt-2">
            <div class="alert alert-success justify-center text-center">
                <span>修改成功！</span>
            </div>
        </div>
    </div>

    <!-- 修改框 -->
    <div class="flex justify-center mt-16">
        <div class="card w-120 bg-base-200 shadow-sm">
            <div class="card-body">
                <h3 class="text-lg font-bold my-1">编辑资料</h3>
                <Photo ref="photo-ref" :photo="user.photo" />
                <Username ref="username-ref" :username="user.username" />
                <Profile ref="profile-ref" :profile="user.profile" />
                
                <p v-if="errorMessage" class="text-red-500">{{ errorMessage }}</p>

                <div class="flex justify-center">
                    <div @click="handleUpdate" class="btn btn-primary w-60 mt-2">更新</div>
                </div>
            </div>
        </div>
    </div>
    
</template>

<style scoped>

</style>