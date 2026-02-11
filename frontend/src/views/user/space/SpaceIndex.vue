<script setup lang="ts">
import { useRoute } from 'vue-router';
import UserInfoField from './components/UserInfoField.vue';
import { ref, useTemplateRef, nextTick, onMounted, onBeforeMount, onBeforeUnmount } from 'vue';
import api from '@/ts/http/api'
import Character from '@/components/character/character.vue';


const route = useRoute(); // 获取路由参数

const userProfile = ref(null)
const characters: any = ref([])
const isLoading = ref(false)
const hasCharacters = ref(true)
const sentinelRef = useTemplateRef('sentinel-ref')

function checkSentinelVisible() {  // 判断哨兵是否能被看到
  if (!sentinelRef.value) return false

  const rect = sentinelRef.value.getBoundingClientRect()
  return rect.top < window.innerHeight && rect.bottom > 0
}

async function loadMore() {
    if (isLoading.value || !hasCharacters.value) return
    isLoading.value = true

    let newCharacters = []
    try {
        const res = await api.get('/api/create/character/get_list/', {
            params: {
                items_count: characters.value.length,
                user_id: route.params.user_id,
            }
        })
        const data = res.data

        console.log(data)
        
        if (data.result === 'success') {
            userProfile.value = data.user_profile
            newCharacters = data.characters
        }
    } catch (err) {
        console.log(err)
    } finally {
        isLoading.value = false
        if (newCharacters.length === 0) {
            hasCharacters.value = false
        } else {
            characters.value.push(...newCharacters)
            await nextTick()

            if (checkSentinelVisible()) {
                await loadMore()
            }
        }
    }
}

let observer: any = null
onMounted(async () => {
    await loadMore()

    observer = new IntersectionObserver(
        // 回调函数，当哨兵元素进入视口时触发
        entries => {
            // 遍历所有观察的元素
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    loadMore()
                    // console.log('红色出现了')
                }
            })
        },
        {
            root: null,
            rootMargin: '2px',
            threshold: 0,
        }
    )
    observer.observe(sentinelRef.value)
})

function removeCharacter(characterId: any) {
    characters.value = characters.value.filter((c: any) => c.id !== characterId)
}

onBeforeUnmount(() => {
    observer?.disconnect() // 释放资源
})

</script>

<template>
    <div class="flex flex-col items-center mb-12">
        <UserInfoField :userProfile="userProfile" />
        <div class="grid grid-cols-[repeat(auto-fill,minmax(240px,1fr))] gap-9 mt-12 justify-items-center w-full px-9">
            <Character 
                v-for="character in characters"
                :key="character.character_id"
                :character="character"
                :canEdit="true"
                @remove="removeCharacter"
            />
        </div>
        <div ref="sentinel-ref" class="h-2 mt-8"></div>
        <div v-if="isLoading" class="text-gray-500 mt-4">加载中...</div>
        <div v-else-if="!hasCharacters" class="text-gray-500 mt-4">没有更多角色了</div>
    </div>
</template>

<style scoped>

</style>