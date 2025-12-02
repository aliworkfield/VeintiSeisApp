import { Box, Flex, Icon, Text } from "@chakra-ui/react"
import { useQueryClient } from "@tanstack/react-query"
import { Link as RouterLink } from "@tanstack/react-router"
import { FiBriefcase, FiHome, FiSettings, FiUsers, FiTag } from "react-icons/fi"
import type { IconType } from "react-icons/lib"

import type { UserOutOld } from "@/client"
import useAuth from "@/hooks/useAuth"

interface Item {
  icon: IconType
  title: string
  path: string
}

const SidebarItems = ({ onClose }: { onClose?: () => void }) => {
  const queryClient = useQueryClient()
  const { user } = useAuth()
  const currentUser = queryClient.getQueryData<UserOutOld>(["currentUser"])

  // Add coupon management links based on user role
  const couponItems = []
  
  // All users can access their own coupons
  couponItems.push({ icon: FiTag, title: "My Coupons", path: "/coupons/me" })
  
  // Managers and admins can access additional coupon features
  if (user?.roles.includes("coupon_manager") || user?.roles.includes("coupon_admin")) {
    couponItems.push({ icon: FiTag, title: "All Coupons", path: "/coupons/all" })
    couponItems.push({ icon: FiTag, title: "Bulk Upload", path: "/coupons/upload" })
    couponItems.push({ icon: FiTag, title: "Campaign Assignment", path: "/coupons/assign" })
  }
  
  // Only admins can access the admin panel
  if (user?.roles.includes("coupon_admin")) {
    couponItems.push({ icon: FiUsers, title: "Coupon Admin", path: "/admin/coupons" })
  }

  const finalItems: Item[] = [
    { icon: FiHome, title: "Dashboard", path: "/" },
    { icon: FiBriefcase, title: "Items", path: "/items" },
    ...couponItems,
    { icon: FiSettings, title: "User Settings", path: "/settings" },
  ]

  // Add admin link for superusers
  if (currentUser?.is_superuser) {
    finalItems.push({ icon: FiUsers, title: "Admin", path: "/admin" })
  }

  const listItems = finalItems.map(({ icon, title, path }) => (
    <RouterLink key={title} to={path} onClick={onClose}>
      <Flex
        gap={4}
        px={4}
        py={2}
        _hover={{
          background: "gray.subtle",
        }}
        alignItems="center"
        fontSize="sm"
      >
        <Icon as={icon} alignSelf="center" />
        <Text ml={2}>{title}</Text>
      </Flex>
    </RouterLink>
  ))

  return (
    <>
      <Text fontSize="xs" px={4} py={2} fontWeight="bold">
        Menu
      </Text>
      <Box>{listItems}</Box>
    </>
  )
}

export default SidebarItems