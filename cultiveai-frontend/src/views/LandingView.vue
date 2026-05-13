<template>
  <div class="min-h-screen bg-white dark:bg-bg-dark text-slate-800 dark:text-slate-200">
    <!-- ============= HEADER ============= -->
    <header
      class="sticky top-0 z-50 bg-white/85 dark:bg-slate-900/85 ios-blur border-b border-slate-100 dark:border-slate-800"
    >
      <div class="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
        <router-link to="/sobre" class="flex items-center gap-2.5">
          <div class="bg-primary p-1.5">
            <span class="material-icons-round text-white text-xl">eco</span>
          </div>
          <span class="text-xl font-bold tracking-tight">
            <span class="text-primary">Cultive</span><span class="text-secondary">AI</span>
          </span>
        </router-link>

        <nav class="hidden md:flex items-center gap-8">
          <a href="#features" class="text-sm font-medium text-slate-600 dark:text-slate-300 hover:text-primary transition-colors">Recursos</a>
          <a href="#how" class="text-sm font-medium text-slate-600 dark:text-slate-300 hover:text-primary transition-colors">Como funciona</a>
          <a href="#use-cases" class="text-sm font-medium text-slate-600 dark:text-slate-300 hover:text-primary transition-colors">Para quem</a>
          <a href="#tech" class="text-sm font-medium text-slate-600 dark:text-slate-300 hover:text-primary transition-colors">Tecnologia</a>
        </nav>

        <div class="flex items-center gap-2.5">
          <router-link
            to="/login"
            class="hidden sm:inline-flex text-sm font-medium text-slate-600 dark:text-slate-300 hover:text-primary px-3 py-2 transition-colors"
          >Entrar</router-link>
          <router-link
            to="/register"
            class="text-sm font-semibold bg-primary hover:bg-primary-dark text-white px-4 py-2.5 transition-colors"
          >Criar conta</router-link>
        </div>
      </div>
    </header>

    <!-- ============= HERO ============= -->
    <section class="relative overflow-hidden bg-gradient-to-br from-primary-dark via-primary to-primary-light text-white">
      <div class="absolute -top-40 -right-40 w-[520px] h-[520px] rounded-full bg-accent/25 blur-3xl pointer-events-none"></div>
      <div class="absolute -bottom-40 -left-32 w-[460px] h-[460px] rounded-full bg-secondary/40 blur-3xl pointer-events-none"></div>
      <svg class="absolute bottom-0 left-0 w-full opacity-25 pointer-events-none" viewBox="0 0 1440 320" preserveAspectRatio="none">
        <path d="M0,224 C400,80 1040,420 1440,180 L1440,320 L0,320 Z" fill="#95D5B2" />
        <path d="M0,260 C480,128 960,400 1440,224 L1440,320 L0,320 Z" fill="white" opacity="0.18" />
      </svg>

      <div class="relative max-w-6xl mx-auto px-6 py-20 md:py-28 grid md:grid-cols-2 gap-12 items-center">
        <div data-animate>
          <span class="inline-block text-[10px] tracking-[0.3em] font-semibold bg-white/15 ring-1 ring-white/30 backdrop-blur-sm px-3 py-1.5">
            PLATAFORMA DE ANÁLISE
          </span>
          <h1 class="mt-6 text-4xl md:text-6xl leading-[1.05]">
            <span class="font-light">Inteligência que</span><br />
            <span class="font-extrabold">Cultiva Resultados</span>
          </h1>
          <p class="mt-6 text-lg text-white/85 leading-relaxed max-w-xl">
            Monitore a saúde das pastagens em tempo real com sensoriamento remoto, índices vegetativos NDVI / NDMI / SAVI e análises geradas por IA.
          </p>
          <div class="mt-8 flex flex-wrap gap-3">
            <router-link
              to="/register"
              class="px-7 py-3.5 bg-white text-primary font-semibold text-sm tracking-[0.2em] hover:bg-accent transition-colors"
            >COMEÇAR AGORA</router-link>
            <a
              href="#how"
              class="px-7 py-3.5 bg-white/10 hover:bg-white/20 backdrop-blur-sm ring-1 ring-white/40 text-white font-medium text-sm transition-colors inline-flex items-center gap-2"
            >
              Ver como funciona
              <span class="material-icons-round text-base">arrow_downward</span>
            </a>
          </div>
          <div class="mt-10 flex flex-wrap items-center gap-6 text-white/75 text-sm">
            <div class="flex items-center gap-2">
              <span class="material-icons-round text-accent text-lg">verified</span>
              Sem custo para começar
            </div>
            <div class="flex items-center gap-2">
              <span class="material-icons-round text-accent text-lg">bolt</span>
              Análise em segundos
            </div>
          </div>
        </div>

        <!-- Hero visual: stylized map preview -->
        <div data-animate data-animate-delay="200" class="relative">
          <div class="bg-white/8 backdrop-blur-md ring-1 ring-white/25 p-5 shadow-2xl">
            <div class="aspect-[4/3] relative overflow-hidden bg-primary-dark">
              <!-- Stylized degradation map -->
              <svg class="absolute inset-0 w-full h-full" viewBox="0 0 400 300" preserveAspectRatio="none">
                <defs>
                  <linearGradient id="g1" x1="0" x2="1" y1="0" y2="1">
                    <stop offset="0" stop-color="#1a9850" />
                    <stop offset="1" stop-color="#66bd63" />
                  </linearGradient>
                  <linearGradient id="g2" x1="0" x2="1" y1="0" y2="1">
                    <stop offset="0" stop-color="#fdae61" />
                    <stop offset="1" stop-color="#d73027" />
                  </linearGradient>
                </defs>
                <path d="M0,40 L120,30 L180,90 L260,60 L400,120 L400,0 L0,0 Z" fill="url(#g1)" opacity="0.85" />
                <path d="M0,140 L80,110 L150,170 L240,150 L320,200 L400,180 L400,80 L0,80 Z" fill="#fee08b" opacity="0.7" />
                <path d="M80,210 L160,200 L240,250 L340,230 L400,280 L400,180 L80,180 Z" fill="url(#g2)" opacity="0.8" />
                <path d="M0,260 L100,240 L180,290 L300,270 L400,300 L400,220 L0,220 Z" fill="#a50026" opacity="0.6" />
                <!-- Pulse markers -->
                <circle cx="120" cy="90" r="6" fill="white" />
                <circle cx="120" cy="90" r="14" fill="white" opacity="0.25" class="pulse-marker" />
                <circle cx="260" cy="170" r="6" fill="white" />
                <circle cx="260" cy="170" r="14" fill="white" opacity="0.25" class="pulse-marker pulse-marker-2" />
              </svg>
              <!-- Overlay metric chip -->
              <div class="absolute top-3 left-3 bg-black/40 backdrop-blur-sm px-3 py-2 text-xs text-white">
                <div class="text-[9px] tracking-widest opacity-75">NDVI MÉDIO</div>
                <div class="font-bold text-base">0,74</div>
              </div>
              <div class="absolute bottom-3 right-3 bg-black/40 backdrop-blur-sm px-3 py-2 text-xs text-white">
                <div class="text-[9px] tracking-widest opacity-75">ÁREA</div>
                <div class="font-bold text-base">128,5 ha</div>
              </div>
            </div>
            <div class="mt-4 grid grid-cols-3 gap-2">
              <div class="bg-white/10 px-3 py-2.5">
                <div class="text-[9px] tracking-widest opacity-70">DEGRADAÇÃO</div>
                <div class="text-sm font-semibold">Baixa</div>
              </div>
              <div class="bg-white/10 px-3 py-2.5">
                <div class="text-[9px] tracking-widest opacity-70">UMIDADE</div>
                <div class="text-sm font-semibold">Ótima</div>
              </div>
              <div class="bg-white/10 px-3 py-2.5">
                <div class="text-[9px] tracking-widest opacity-70">SATÉLITE</div>
                <div class="text-sm font-semibold">Sentinel-2</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ============= STATS ============= -->
    <section class="bg-white dark:bg-slate-900 border-b border-slate-100 dark:border-slate-800">
      <div class="max-w-6xl mx-auto px-6 py-14 grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
        <div data-animate>
          <div class="text-3xl md:text-4xl font-extrabold text-primary">99,7%</div>
          <div class="text-xs tracking-widest uppercase text-slate-400 mt-2">Precisão NDVI</div>
        </div>
        <div data-animate data-animate-delay="100">
          <div class="text-3xl md:text-4xl font-extrabold text-primary">10 m</div>
          <div class="text-xs tracking-widest uppercase text-slate-400 mt-2">Resolução por pixel</div>
        </div>
        <div data-animate data-animate-delay="200">
          <div class="text-3xl md:text-4xl font-extrabold text-primary">5 dias</div>
          <div class="text-xs tracking-widest uppercase text-slate-400 mt-2">Revisita do satélite</div>
        </div>
        <div data-animate data-animate-delay="300">
          <div class="text-3xl md:text-4xl font-extrabold text-primary">&lt; 30 s</div>
          <div class="text-xs tracking-widest uppercase text-slate-400 mt-2">Geração da análise</div>
        </div>
      </div>
    </section>

    <!-- ============= HOW IT WORKS ============= -->
    <section id="how" class="py-24 bg-slate-50 dark:bg-slate-950">
      <div class="max-w-6xl mx-auto px-6">
        <header data-animate class="text-center max-w-2xl mx-auto mb-16">
          <span class="text-[10px] tracking-[0.3em] font-semibold text-primary">FLUXO</span>
          <h2 class="mt-3 text-3xl md:text-4xl font-bold">Como funciona</h2>
          <p class="mt-4 text-slate-500 dark:text-slate-400">
            Da seleção da área até o relatório completo em quatro passos simples.
          </p>
        </header>

        <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-5">
          <div
            v-for="(step, i) in steps"
            :key="step.title"
            data-animate
            :data-animate-delay="i * 120"
            class="relative bg-white dark:bg-slate-900 p-7 border border-slate-100 dark:border-slate-800 hover:border-primary/40 transition-all hover:-translate-y-1"
          >
            <div class="absolute -top-4 left-7 bg-primary text-white text-xs font-bold tracking-widest px-2.5 py-1">
              0{{ i + 1 }}
            </div>
            <div class="inline-flex w-12 h-12 items-center justify-center bg-primary-bg dark:bg-primary/10 text-primary mb-5 mt-2">
              <span class="material-icons-round text-2xl">{{ step.icon }}</span>
            </div>
            <h3 class="text-lg font-bold">{{ step.title }}</h3>
            <p class="mt-2 text-sm text-slate-500 dark:text-slate-400 leading-relaxed">{{ step.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- ============= FEATURES ============= -->
    <section id="features" class="py-24 bg-white dark:bg-slate-900">
      <div class="max-w-6xl mx-auto px-6">
        <header data-animate class="text-center max-w-2xl mx-auto mb-16">
          <span class="text-[10px] tracking-[0.3em] font-semibold text-primary">RECURSOS</span>
          <h2 class="mt-3 text-3xl md:text-4xl font-bold">Tudo que você precisa para decidir</h2>
          <p class="mt-4 text-slate-500 dark:text-slate-400">
            Índices vegetativos, classificação de degradação, descrição por IA e relatórios prontos para o campo.
          </p>
        </header>

        <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-5">
          <div
            v-for="(f, i) in features"
            :key="f.title"
            data-animate
            :data-animate-delay="(i % 3) * 120"
            class="group relative p-7 bg-slate-50 dark:bg-slate-950 border border-slate-100 dark:border-slate-800 hover:border-primary/40 hover:bg-white dark:hover:bg-slate-900 transition-all overflow-hidden"
          >
            <div class="absolute -right-10 -top-10 w-32 h-32 rounded-full bg-accent/20 blur-2xl opacity-0 group-hover:opacity-100 transition-opacity"></div>
            <div class="relative">
              <div class="inline-flex w-12 h-12 items-center justify-center bg-primary text-white mb-5">
                <span class="material-icons-round text-2xl">{{ f.icon }}</span>
              </div>
              <h3 class="text-lg font-bold">{{ f.title }}</h3>
              <p class="mt-2 text-sm text-slate-500 dark:text-slate-400 leading-relaxed">{{ f.desc }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ============= USE CASES ============= -->
    <section id="use-cases" class="py-24 bg-slate-50 dark:bg-slate-950">
      <div class="max-w-6xl mx-auto px-6">
        <header data-animate class="text-center max-w-2xl mx-auto mb-16">
          <span class="text-[10px] tracking-[0.3em] font-semibold text-primary">PARA QUEM</span>
          <h2 class="mt-3 text-3xl md:text-4xl font-bold">Pensado para o campo</h2>
          <p class="mt-4 text-slate-500 dark:text-slate-400">
            Agrônomos, produtores e pesquisadores tomando decisões mais rápidas com dados confiáveis.
          </p>
        </header>

        <div class="grid md:grid-cols-3 gap-5">
          <div
            v-for="(uc, i) in useCases"
            :key="uc.title"
            data-animate
            :data-animate-delay="i * 150"
            class="bg-white dark:bg-slate-900 p-8 border border-slate-100 dark:border-slate-800 flex flex-col"
          >
            <div class="inline-flex w-14 h-14 items-center justify-center bg-primary-bg dark:bg-primary/10 text-primary">
              <span class="material-icons-round text-3xl">{{ uc.icon }}</span>
            </div>
            <h3 class="mt-5 text-xl font-bold">{{ uc.title }}</h3>
            <p class="mt-2 text-sm text-slate-500 dark:text-slate-400 leading-relaxed flex-1">{{ uc.desc }}</p>
            <ul class="mt-5 space-y-2">
              <li
                v-for="point in uc.points"
                :key="point"
                class="flex items-start gap-2 text-sm text-slate-600 dark:text-slate-300"
              >
                <span class="material-icons-round text-primary text-base mt-0.5">check_circle</span>
                {{ point }}
              </li>
            </ul>
          </div>
        </div>
      </div>
    </section>

    <!-- ============= TECH STACK ============= -->
    <section id="tech" class="py-20 bg-white dark:bg-slate-900 border-y border-slate-100 dark:border-slate-800">
      <div class="max-w-6xl mx-auto px-6">
        <header data-animate class="text-center max-w-2xl mx-auto mb-12">
          <span class="text-[10px] tracking-[0.3em] font-semibold text-primary">TECNOLOGIA</span>
          <h2 class="mt-3 text-3xl md:text-4xl font-bold">Construído sobre o que há de melhor</h2>
        </header>

        <div data-animate class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div
            v-for="t in tech"
            :key="t.name"
            class="bg-slate-50 dark:bg-slate-950 p-6 border border-slate-100 dark:border-slate-800 text-center"
          >
            <span class="material-icons-round text-primary text-3xl">{{ t.icon }}</span>
            <div class="mt-3 font-bold text-sm">{{ t.name }}</div>
            <div class="text-xs text-slate-400 mt-1">{{ t.role }}</div>
          </div>
        </div>
      </div>
    </section>

    <!-- ============= CTA ============= -->
    <section class="relative py-24 overflow-hidden bg-gradient-to-br from-primary-dark via-primary to-primary-light text-white">
      <div class="absolute -top-32 right-0 w-[400px] h-[400px] rounded-full bg-accent/30 blur-3xl pointer-events-none"></div>
      <div class="absolute -bottom-32 left-0 w-[400px] h-[400px] rounded-full bg-secondary/40 blur-3xl pointer-events-none"></div>

      <div data-animate class="relative max-w-3xl mx-auto px-6 text-center">
        <h2 class="text-3xl md:text-5xl leading-tight">
          <span class="font-light">Pronto para</span>
          <span class="font-extrabold">cultivar resultados?</span>
        </h2>
        <p class="mt-5 text-white/85 text-lg leading-relaxed">
          Crie sua conta gratuitamente e gere a primeira análise da sua pastagem em menos de um minuto.
        </p>
        <div class="mt-8 flex flex-wrap gap-3 justify-center">
          <router-link
            to="/register"
            class="px-8 py-4 bg-white text-primary font-semibold text-sm tracking-[0.2em] hover:bg-accent transition-colors"
          >CRIAR CONTA</router-link>
          <router-link
            to="/login"
            class="px-8 py-4 bg-white/10 hover:bg-white/20 backdrop-blur-sm ring-1 ring-white/40 text-white font-medium text-sm transition-colors"
          >Já tenho conta</router-link>
        </div>
      </div>
    </section>

    <!-- ============= FOOTER ============= -->
    <footer class="bg-slate-950 text-slate-400">
      <div class="max-w-6xl mx-auto px-6 py-16 grid md:grid-cols-4 gap-10">
        <div class="md:col-span-2">
          <div class="flex items-center gap-2.5">
            <div class="bg-primary p-1.5">
              <span class="material-icons-round text-white text-xl">eco</span>
            </div>
            <span class="text-xl font-bold tracking-tight text-white">
              <span class="text-primary-light">Cultive</span><span class="text-accent">AI</span>
            </span>
          </div>
          <p class="mt-4 text-sm leading-relaxed max-w-md">
            Plataforma de análise inteligente de pastagens. Monitoramento de NDVI, classificação de degradação e descrição por IA Gemini.
          </p>
        </div>

        <div>
          <div class="text-xs tracking-widest font-semibold text-white uppercase mb-4">Produto</div>
          <ul class="space-y-2 text-sm">
            <li><a href="#features" class="hover:text-primary-light transition-colors">Recursos</a></li>
            <li><a href="#how" class="hover:text-primary-light transition-colors">Como funciona</a></li>
            <li><a href="#use-cases" class="hover:text-primary-light transition-colors">Para quem</a></li>
            <li><a href="#tech" class="hover:text-primary-light transition-colors">Tecnologia</a></li>
          </ul>
        </div>

        <div>
          <div class="text-xs tracking-widest font-semibold text-white uppercase mb-4">Conta</div>
          <ul class="space-y-2 text-sm">
            <li><router-link to="/login" class="hover:text-primary-light transition-colors">Entrar</router-link></li>
            <li><router-link to="/register" class="hover:text-primary-light transition-colors">Criar conta</router-link></li>
            <li><router-link to="/forgot-password" class="hover:text-primary-light transition-colors">Esqueci a senha</router-link></li>
          </ul>
        </div>
      </div>
      <div class="border-t border-slate-800">
        <div class="max-w-6xl mx-auto px-6 py-6 flex flex-col md:flex-row items-center justify-between gap-3 text-xs text-slate-500">
          <span>© {{ year }} CultiveAI. Todos os direitos reservados.</span>
          <span>Dados: Sentinel-2 (Copernicus/ESA) · Google Earth Engine · IA Gemini</span>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { onMounted, onBeforeUnmount, ref } from "vue";

const year = new Date().getFullYear();

const steps = [
  { icon: "edit_location_alt", title: "Desenhe a área", desc: "Selecione no mapa o talhão ou propriedade que você quer monitorar." },
  { icon: "satellite_alt", title: "Imagens Sentinel-2", desc: "Buscamos a cena mais recente, com baixa cobertura de nuvens, via Google Earth Engine." },
  { icon: "psychology", title: "Cálculo + IA", desc: "Calculamos NDVI, NDMI, SAVI e classificamos a degradação. IA Gemini gera a descrição." },
  { icon: "summarize", title: "Relatório completo", desc: "Mapa interativo, dashboard com estatísticas e PDF pronto para compartilhar." },
];

const features = [
  { icon: "eco", title: "NDVI e classificação", desc: "Índice de vegetação por diferença normalizada e seis classes de degradação automáticas." },
  { icon: "water_drop", title: "NDMI e SAVI", desc: "Análise complementar de umidade do dossel e índice ajustado para solos expostos." },
  { icon: "auto_awesome", title: "Descrição por IA", desc: "Resumo textual inteligente da saúde da pastagem gerado pela IA Gemini." },
  { icon: "map", title: "Mapa interativo", desc: "Camadas Folium/Leaflet com toggles de NDVI, degradação, declividade e MapBiomas." },
  { icon: "picture_as_pdf", title: "Relatório PDF", desc: "Exporte um documento profissional com gráficos, mapas e a descrição da IA." },
  { icon: "folder_managed", title: "Clientes e propriedades", desc: "Organize análises por cliente e por propriedade, com histórico completo." },
];

const useCases = [
  {
    icon: "agriculture",
    title: "Produtores rurais",
    desc: "Monitore a saúde da pastagem do celular e priorize manejos com base em dados.",
    points: ["Visão por talhão", "Histórico ao longo do ano", "Alerta de degradação"],
  },
  {
    icon: "engineering",
    title: "Agrônomos e consultores",
    desc: "Diagnósticos rápidos e relatórios prontos para entregar ao cliente.",
    points: ["Comparação entre datas", "PDF com sua marca", "Acesso multi-cliente"],
  },
  {
    icon: "science",
    title: "Pesquisadores",
    desc: "Reproduza análises em larga escala com dados abertos e auditáveis.",
    points: ["Sentinel-2 harmonizado", "Limiares ajustáveis", "Exportação de estatísticas"],
  },
];

const tech = [
  { icon: "satellite_alt", name: "Sentinel-2", role: "Imagens ópticas" },
  { icon: "public", name: "Earth Engine", role: "Processamento" },
  { icon: "auto_awesome", name: "Gemini", role: "IA generativa" },
  { icon: "bolt", name: "FastAPI + Vue", role: "Stack moderna" },
];

let observer;

onMounted(() => {
  const elements = document.querySelectorAll("[data-animate]");
  elements.forEach((el) => {
    const delay = el.getAttribute("data-animate-delay");
    if (delay) el.style.transitionDelay = `${delay}ms`;
  });

  observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.15, rootMargin: "0px 0px -50px 0px" }
  );
  elements.forEach((el) => observer.observe(el));

  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach((a) => {
    a.addEventListener("click", smoothScroll);
  });
});

onBeforeUnmount(() => {
  if (observer) observer.disconnect();
  document.querySelectorAll('a[href^="#"]').forEach((a) => {
    a.removeEventListener("click", smoothScroll);
  });
});

function smoothScroll(e) {
  const href = e.currentTarget.getAttribute("href");
  if (!href || href === "#") return;
  const target = document.querySelector(href);
  if (!target) return;
  e.preventDefault();
  target.scrollIntoView({ behavior: "smooth", block: "start" });
}
</script>

<style scoped>
[data-animate] {
  opacity: 0;
  transform: translateY(28px);
  transition: opacity 0.8s ease, transform 0.8s ease;
  will-change: opacity, transform;
}
[data-animate].is-visible {
  opacity: 1;
  transform: translateY(0);
}

.pulse-marker {
  transform-origin: center;
  animation: pulse 2.4s ease-out infinite;
}
.pulse-marker-2 {
  animation-delay: 1.2s;
}
@keyframes pulse {
  0% {
    transform: scale(0.6);
    opacity: 0.55;
  }
  70% {
    transform: scale(2.2);
    opacity: 0;
  }
  100% {
    transform: scale(2.2);
    opacity: 0;
  }
}

@media (prefers-reduced-motion: reduce) {
  [data-animate] {
    opacity: 1;
    transform: none;
    transition: none;
  }
  .pulse-marker {
    animation: none;
  }
}
</style>
