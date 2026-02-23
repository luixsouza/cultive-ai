import { createRouter, createWebHistory } from "vue-router";
import { isLoggedIn } from "../services/auth";

const routes = [
  {
    path: "/login",
    name: "Login",
    component: () => import("../views/LoginView.vue"),
    meta: { guest: true },
  },
  {
    path: "/register",
    name: "Register",
    component: () => import("../views/RegisterView.vue"),
    meta: { guest: true },
  },
  {
    path: "/",
    name: "Dashboard",
    component: () => import("../views/DashboardView.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/clients",
    name: "Clients",
    component: () => import("../views/ClientsView.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/clients/:clientId/properties",
    name: "ClientProperties",
    component: () => import("../views/PropertiesView.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/properties",
    name: "Properties",
    component: () => import("../views/PropertiesView.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/analysis/new",
    name: "NewAnalysis",
    component: () => import("../views/HomeView.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/analysis/:id",
    name: "AnalysisView",
    component: () => import("../views/AnalysisView.vue"),
    props: true,
    meta: { requiresAuth: true },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  if (to.matched.some((record) => record.meta.requiresAuth)) {
    if (!isLoggedIn()) {
      next({ name: "Login", query: { redirect: to.fullPath } });
    } else {
      next();
    }
  } else if (to.matched.some((record) => record.meta.guest)) {
    if (isLoggedIn()) {
      next({ name: "Dashboard" });
    } else {
      next();
    }
  } else {
    next();
  }
});

export default router;
