import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import { isLoggedIn } from "../services/auth";

const routes = [
  {
    path: "/login",
    name: "LoginView",
    component: () => import("../views/LoginView.vue"),
  },
  {
    path: "/",
    name: "HomeView",
    component: HomeView,
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
      next({ name: "LoginView" });
    } else {
      next();
    }
  } else {
    next();
  }
});

export default router;
