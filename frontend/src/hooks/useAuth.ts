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
import useCustomToast from "./useCustomToast"

const isLoggedIn = () => {
  return localStorage.getItem("access_token") !== null
}

const useAuth = () => {
  const [error, setError] = useState<string | null>(null)
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const { showErrorToast } = useCustomToast()
  
  const { data: user, isLoading, refetch } = useQuery<UserPublic | null, Error>({
    queryKey: ["currentUser"],
    queryFn: async () => {
      // For Windows Auth, we don't need to send the X-Windows-User header
      // IIS will inject it automatically. We just need to make the request
      // and let the backend handle the authentication.
      
      // First, try to get user info with existing token if available
      if (isLoggedIn()) {
        try {
          return await UsersService.readUserMe()
        } catch (error) {
          // If token-based auth fails, continue to Windows auth check
        }
      }
      
      // Try Windows authentication by calling the Windows login endpoint
      try {
        const res = await fetch(`/api/v1/login/windows`, { 
          credentials: "include",
          headers: {
            "Content-Type": "application/json",
          }
        })
        
        // If we get a successful response, we're authenticated with Windows Auth
        if (res.ok) {
          const data = await res.json()
          // Store the JWT token we received
          localStorage.setItem("access_token", data.token)
          return data.user
        }
        
        // For any other status, return null (not authenticated)
        return null
      } catch (error) {
        // Network error or other issue
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

  const loginWithWindows = async () => {
    try {
      const response = await fetch("/api/v1/login/windows", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include"
      });

      if (response.ok) {
        const data = await response.json();
        // Store the JWT token
        localStorage.setItem("access_token", data.token);
        // Refresh the user data
        queryClient.invalidateQueries({ queryKey: ["currentUser"] });
        // Navigate to home
        navigate({ to: "/" });
        return { success: true, data };
      } else {
        const errorData = await response.json();
        showErrorToast(errorData.detail || "Windows login failed");
        return { success: false, error: errorData };
      }
    } catch (error: any) {
      showErrorToast(error.message || "Windows login failed");
      return { success: false, error };
    }
  };

  const logout = () => {
    localStorage.removeItem("access_token")
    navigate({ to: "/login" })
  }

  return {
    signUpMutation,
    loginMutation,
    loginWithWindows,
    logout,
    user,
    error,
    isLoading,
    resetError: () => setError(null),
  }
}

export { isLoggedIn }
export default useAuth