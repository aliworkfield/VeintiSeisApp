import { Container, Image, Input, Text } from "@chakra-ui/react"
import {
  Link as RouterLink,
  createFileRoute,
  redirect,
} from "@tanstack/react-router"
import { type SubmitHandler, useForm } from "react-hook-form"
import { FiLock, FiMail } from "react-icons/fi"
import { useEffect, useState } from "react"

import { Button } from "@/components/ui/button"
import { Field } from "@/components/ui/field"
import { InputGroup } from "@/components/ui/input-group"
import { PasswordInput } from "@/components/ui/password-input"
import useAuth, { isLoggedIn } from "@/hooks/useAuth"
import Logo from "/assets/images/fastapi-logo.svg"
import { emailPattern, passwordRules } from "../utils"

export const Route = createFileRoute("/login")({
  component: Login,
  beforeLoad: async () => {
    if (isLoggedIn()) {
      throw redirect({
        to: "/",
      })
    }
  },
})

function Login() {
  const { loginMutation, loginWithWindows, error, resetError, user } = useAuth()
  const [isWindowsAuthLoading, setIsWindowsAuthLoading] = useState(false)
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm({
    mode: "onBlur",
    criteriaMode: "all",
    defaultValues: {
      username: "",
      password: "",
    },
  })

  // Redirect to home if user is authenticated (including Windows auth)
  useEffect(() => {
    if (user) {
      // User is authenticated, redirect to home
      window.location.href = "/";
    }
  }, [user]);

  const handleWindowsAuth = async () => {
    setIsWindowsAuthLoading(true);
    try {
      // Use the loginWithWindows function from the useAuth hook
      const result = await loginWithWindows();
      if (!result.success) {
        console.error("Windows authentication error:", result.error);
      }
    } catch (err) {
      console.error("Windows authentication error:", err);
    } finally {
      setIsWindowsAuthLoading(false);
    }
  };

  const onSubmit: SubmitHandler<any> = async () => {
    if (isSubmitting) return

    resetError()

    try {
      // The loginMutation doesn't take any parameters, it just triggers the login process
      await loginMutation.mutateAsync()
    } catch {
      // error is handled by useAuth hook
    }
  }

  return (
    <>
      <Container
        as="form"
        onSubmit={handleSubmit(onSubmit)}
        h="100vh"
        maxW="sm"
        alignItems="stretch"
        justifyContent="center"
        gap={4}
        centerContent
      >
        <Image
          src={Logo}
          alt="FastAPI logo"
          height="auto"
          maxW="2xs"
          alignSelf="center"
          mb={4}
        />
        <Button 
          variant="outline" 
          onClick={handleWindowsAuth} 
          loading={isWindowsAuthLoading}
          size="md"
          mb={4}
        >
          Login with Windows Authentication
        </Button>
        <Field
          invalid={!!errors.username}
          errorText={errors.username?.message || !!error}
        >
          <InputGroup w="100%" startElement={<FiMail />}>
            <Input
              id="username"
              {...register("username", {
                required: "Username is required",
                pattern: emailPattern,
              })}
              placeholder="Email"
              type="email"
            />
          </InputGroup>
        </Field>
        <PasswordInput
          type="password"
          startElement={<FiLock />}
          {...register("password", passwordRules())}
          placeholder="Password"
          errors={errors}
        />
        <RouterLink to="/recover-password" className="main-link">
          Forgot Password?
        </RouterLink>
        <Button variant="solid" type="submit" loading={isSubmitting} size="md">
          Log In
        </Button>
        <Text>
          Don't have an account?{" "}
          <RouterLink to="/signup" className="main-link">
            Sign Up
          </RouterLink>
        </Text>
      </Container>
    </>
  )
}

export default Login