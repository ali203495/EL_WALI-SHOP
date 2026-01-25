// @ts-nocheck
export default defineNuxtPlugin((_nuxtApp) => {
    const config = useRuntimeConfig()
    const pixelId = config.public.facebookPixelId

    if (!pixelId) {
        // console.warn('Facebook Pixel ID is not set. Pixel disabled.')
        return
    }

    // Inject Facebook Pixel
    /* eslint-disable */
    !function (f, b, e, v, n, t, s) {
        if (f.fbq) return; n = f.fbq = function () {
            n.callMethod ?
                n.callMethod.apply(n, arguments) : n.queue.push(arguments)
        };
        if (!f._fbq) f._fbq = n; n.push = n; n.loaded = !0; n.version = '2.0';
        n.queue = []; t = b.createElement(e); t.async = !0;
        t.src = v; s = b.getElementsByTagName(e)[0];
        s.parentNode.insertBefore(t, s)
    }(window, document, 'script',
        'https://connect.facebook.net/en_US/fbevents.js');
    /* eslint-enable */

    // Initialize
    if ((window as any).fbq) {
        (window as any).fbq('init', pixelId)
    }

    // Track PageView on route change
    const router = useRouter()
    router.afterEach(() => {
        (window as any).fbq('track', 'PageView')
    })

    // Provide helper for custom events
    return {
        provide: {
            fbq: (event: string, params: any = {}) => {
                if ((window as any).fbq) {
                    (window as any).fbq('track', event, params)
                }
            }
        }
    }
})

declare global {
    interface Window {
        fbq: any
    }
}
