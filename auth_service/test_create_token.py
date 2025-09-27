from app.core.tokens import generate_token_pair


def main():
    user_id = 1
    username = "alice"

    # Sinh cặp token
    tokens = generate_token_pair(user_id, username)

    print(" Access Token:", tokens["accessToken"][:100] + "...")
    print(" Refresh Token:", tokens["refreshToken"][:100] + "...")


if __name__ == "__main__":
    main()