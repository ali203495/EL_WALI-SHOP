import { gsap } from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'

export default defineNuxtPlugin(() => {
    // Only run on client
    if (import.meta.client) {
        gsap.registerPlugin(ScrollTrigger)
    }

    return {
        provide: {
            gsap,
            ScrollTrigger,
        },
    }
})
