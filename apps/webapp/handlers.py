from bson import ObjectId
from dtlib import jsontool
from dtlib.aio.decos import my_async_jsonp
from dtlib.tornado.decos import token_required
from dtlib.tornado.docs import TestDataApp
from dtlib.utils import list_have_none_mem
from dtlib.web.constcls import ConstData
from dtlib.web.tools import get_std_json_response

from xt_base.base_server import MyBaseHandler


class GetCurrentOrgTestApp(MyBaseHandler):
    """
    获取当前组织的自动化APP
    """

    @token_required()
    @my_async_jsonp
    async def get(self):
        organization = await self.get_organization()
        """:type Organization"""
        app = await TestDataApp.objects.get(organization=ObjectId(organization.get_id()))

        if app is None:
            return ConstData.msg_none
        else:
            result = []

            result.append(app.to_dict())
            return get_std_json_response(code=200, data=jsontool.dumps(result))


class GetOrgTestApps(MyBaseHandler):
    """
    获取某个组织的自动化APP
    """

    @token_required()
    @my_async_jsonp
    async def get(self):
        org_id = self.get_argument('org_id', None)

        if list_have_none_mem(*[org_id, ]):
            return ConstData.msg_args_wrong

        # org = await Organization.objects.get(id=ObjectId(str(org_id)))
        # """:type Organization"""
        # if org is None:
        #     return ConstData.msg_none

        test_app = await TestDataApp.objects.get(organization=ObjectId(str(org_id)))  # 如果后面是1对多了,则查询多条

        if test_app is None:
            return ConstData.msg_none
        else:
            # result = []
            # result.append(test_app.to_dict())
            return get_std_json_response(code=200, data=jsontool.dumps(test_app.to_dict(), ensure_ascii=False))
