export interface Toast {
    success(message: string): void
    error(message: string): void
    info(message: string): void
    warning(message: string): void
}

declare module '#app' {
    interface NuxtApp {
        $toast: Toast
    }
}

declare module 'vue' {
    interface ComponentCustomProperties {
        $toast: Toast
    }
}

export { }
