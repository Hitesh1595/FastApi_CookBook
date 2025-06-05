import httpx
from fastapi import APIRouter, HTTPException, status

from security import Token
from third_party_login import (
    GITHUB_AUTHORIZATION_URL,
    GITHUB_CLIENT_ID,
    GITHUB_CLIENT_SECRET,
    GITHUB_REDIRECT_URI,
)

router = APIRouter()

# Take a look at the GitHub documentation that provides a guide on how to set up OAuth2 authentication:
# • GitHub OAuth2 integration: https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/authorizing-oauth-apps

# You can use third-party authorization login with other providers that allow a similar configuration.
# You can check, for example, Google and Twitter:

# • Google OAuth2 integration: https://developers.google.com/identity/protocols/oauth2
# • Twitter OAuth2 integration: https://developer.twitter.com/en/docs/authentication/oauth-2-0



@router.get("/auth/url")
def github_login():
    return {
        "auth_url": GITHUB_AUTHORIZATION_URL + f"?client_id={GITHUB_CLIENT_ID}"
    }



@router.get(
    "/github/auth/token",
    response_model=Token,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "User not registered"
        }
    },
)
async def github_callback(code: str):
    print("github_callback")
    token_response = httpx.post(
        "https://github.com/login/oauth/access_token",
        data={
            "client_id": GITHUB_CLIENT_ID,
            "client_secret": GITHUB_CLIENT_SECRET,
            "code": code,
            "redirect_uri": GITHUB_REDIRECT_URI,
        },
        headers={"Accept": "application/json"},
    ).json()
    access_token = token_response.get("access_token")
    if not access_token:
        raise HTTPException(
            status_code=401,
            detail="User not registered",
        )
    token_type = token_response.get(
        "token_type", "bearer"
    )

    return {
        "access_token": access_token,
        "token_type": token_type,
    }
