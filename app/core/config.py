import os

# JWT settings
JWT_SECRET = os.environ.get("JWT_SECRET", "dev-secret-change-in-production")
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_MINUTES = 60 * 24  # 24 hours

# Verification token expiry
VERIFICATION_TOKEN_EXPIRE_HOURS = 24

# Cookie settings (for local dev: http only, no secure flag needed)
COOKIE_SECURE = os.environ.get("COOKIE_SECURE", "false").lower() == "true"
COOKIE_SAMESITE = "lax"
