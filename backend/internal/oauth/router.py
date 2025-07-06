from fastapi import APIRouter, Depends, Request
from authlib.integrations.starlette_client import OAuth


router = APIRouter()

oauth = OAuth()
oauth.register(
    name="github",
    client_id="Ov23liEF73aSzUcK3I0s",
    client_secret="74cc94928c7547a5675bd60a565b30f9348a57e8",
    access_token_url='https://github.com/login/oauth/access_token',
    access_token_params=None,
    authorize_url='https://github.com/login/oauth/authorize',
    authorize_params=None,
    api_base_url='https://api.github.com/',
    client_kwargs={"scope": "read:user repo"},
)


@router.get("/link/github")
async def link_to_github(request: Request):
    redirect_uri = request.url_for("github_callback")
    return await oauth.github.authorize_redirect(request, redirect_uri)


@router.get("/callback/github")
async def github_callback(request: Request):
    token = await oauth.github.authorize_access_token(request)
    resp = await oauth.github.get("user", token=token)
    profile = resp.json()
    return {"message": "GitHub account linked successfully", "user": profile}