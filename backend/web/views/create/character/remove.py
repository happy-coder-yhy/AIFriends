from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from web.models.character import Character
from web.views.utils.photo import remove_old_photo


class RemoveCharacterView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            character_id = request.data['character_id']
            character = Character.objects.get(pk=character_id, author__user=request.user)
            remove_old_photo(character.photo)  # 删除头像
            remove_old_photo(character.background_image)  # 删除聊天背景
            character.delete()  # 删除角色
            return Response({
                'result': 'success'
            })

        except:
            return Response({
                'result': '系统异常，请重试'
            })

