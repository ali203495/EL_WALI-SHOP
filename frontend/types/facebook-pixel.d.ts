export { }

declare global {
    interface Window {
        fbq: {
            (event: string, eventName: string, params?: Record<string, any>): void
            callMethod?: (...args: any[]) => void
            queue: any[]
            loaded: boolean
            version: string
            push: (...args: any[]) => void
        }
        _fbq: any
    }
}
