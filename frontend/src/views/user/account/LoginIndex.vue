<script setup lang="ts">
import { ref } from 'vue';
import { useUserStore } from '@/stores/user';
import api from '@/ts/http/api.ts';
import { useRouter } from 'vue-router';

const  username = ref('');
const  password = ref('');
const errorMessage = ref('');

const user = useUserStore();
const router = useRouter();

async function handleLogin() {
    errorMessage.value = ''; 
    if (!username.value.trim()) {
        errorMessage.value = '用户名不能为空！';
    } else if (!password.value.trim()) {
        errorMessage.value = '密码不能为空！';
    } else {
        try {
            const res = await api.post('/api/user/account/login/', {
                username: username.value,
                password: password.value
            })
            const data = res.data;
            if (data.result === 'success') {
                user.setAccessToken(data.access);
                user.setUserInfo(data);
                await router.push({ 
                    name: 'homepage-index' 
                });
            } else {
                errorMessage.value = data.result;
            }
        } catch (err) {
            console.log(err);
        }
    }
}
</script>

<template>
    <div @submit.prevent="handleLogin" class="flex justify-center mt-30">
        <form class="fieldset bg-base-200 border-base-300 rounded-box w-xs border p-4">
            <label class="label">用户名</label>
            <input v-model="username" type="text" class="input focus:outline-none" placeholder="用户名" />

            <label class="label">密码</label>
            <input v-model="password" type="password" class="input focus:outline-none" placeholder="密码" />

            <p v-if="errorMessage" class="text-red-600 text-sm mt-1">{{ errorMessage }}</p>

            <button class="btn btn-neutral mt-4 bg-blue-600 border-blue-600 hover:bg-blue-700">登录</button>
            <div class="flex justify-end mt-2">
                <span class="flex items-center text-sky-600">还没有账号？</span>
                <RouterLink :to="{name: 'user-account-register-index'}" class="btn btn-info btn-sm btn-ghost">注册</RouterLink>
            </div>
        </form>
    </div>
</template>

<style scoped>

</style>