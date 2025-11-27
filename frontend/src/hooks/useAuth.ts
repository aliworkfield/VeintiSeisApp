import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { useNavigate } from "@tanstack/react-router"
import { useEffect, useState } from "react"

import {
  type Body_login_login_access_token as AccessToken,
  type ApiError,
  LoginService,
  type UserPublic,
  type UserRegister,
  UsersService,
} from "@/client"
import { handleError } from "@/utils"

const isLoggedIn = () => {
  return localStorage.getItem("access_token") !== null
}

const useAuth = () => {
  const [error, setError] = useState<string | null>(null)
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  
  const { data: user, isLoading, refetch } = useQuery<UserPublic | null, Error>({
    queryKey: ["currentUser"],
    queryFn: async () => {
      // For Windows Auth, we don't need to send the X-Windows-User header
      // IIS will inject it automatically. We just need to make the request
      // and let the backend handle the authentication.
      
      // Try Windows authentication first (this will work if IIS sets the header)
      try {
        const res = await fetch(`/api/v1/me`, { 
          credentials: "include",
          headers: {
            "Content-Type": "application/json",
          }
        })
        
        // If we get a successful response, we're authenticated with Windows Auth
        if (res.ok) {
          return await res.json()
        }
        
        // If we get a 401, it means Windows Auth failed, try token-based auth
        if (res.status === 401 && isLoggedIn()) {
          return await UsersService.readUserMe()
        }
        
        // For any other status, return null (not authenticated)
        return null
      } catch (error) {
        // Network error or other issue - fallback to token-based auth if token exists
        if (isLoggedIn()) {
          try {
            return await UsersService.readUserMe()
          } catch (tokenError) {
            // Both methods failed
            return null
          }
        }
        return null
      }
    },
    retry: false, // Don't retry failed attempts automatically
  })
  
  // Automatically attempt Windows authentication on app load
  useEffect(() => {
    // Only attempt auto-authentication if we don't already have a token
    if (!isLoggedIn()) {
      refetch();
    }
  }, [refetch]);

  const signUpMutation = useMutation({
    mutationFn: (data: UserRegister) =>
      UsersService.registerUser({ requestBody: data }),

    onSuccess: () => {
      navigate({ to: "/login" })
    },
    onError: (err: ApiError) => {
      handleError(err)
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ["users"] })
    },
  })

  const login = async (data: AccessToken) => {
    const response = await LoginService.loginAccessToken({
      formData: data,
    })
    localStorage.setItem("access_token", response.access_token)
  }

  const loginMutation = useMutation({
    mutationFn: login,
    onSuccess: () => {
      navigate({ to: "/" })
    },
    onError: (err: ApiError) => {
      handleError(err)
    },
  })

  const logout = () => {
    localStorage.removeItem("access_token")
    navigate({ to: "/login" })
  }

  return {
    signUpMutation,
    loginMutation,
    logout,
    user,
    error,
    isLoading,
    resetError: () => setError(null),
  }
}

export { isLoggedIn }
export default useAuth