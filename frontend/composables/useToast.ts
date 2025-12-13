interface Toast {
    id: number
    message: string
    type: 'success' | 'error' | 'info' | 'warning'
    duration: number
}

const toasts = ref<Toast[]>([])
let nextId = 0

export const useToast = () => {
    const show = (message: string, type: Toast['type'] = 'info', duration = 3000) => {
        const id = nextId++

        toasts.value.push({ id, message, type, duration })

        setTimeout(() => {
            remove(id)
        }, duration)

        return id
    }

    const remove = (id: number) => {
        const index = toasts.value.findIndex(t => t.id === id)
        if (index > -1) {
            toasts.value.splice(index, 1)
        }
    }

    const success = (message: string, duration?: number) => show(message, 'success', duration)
    const error = (message: string, duration?: number) => show(message, 'error', duration)
    const info = (message: string, duration?: number) => show(message, 'info', duration)
    const warning = (message: string, duration?: number) => show(message, 'warning', duration)

    return {
        toasts: readonly(toasts),
        show,
        remove,
        success,
        error,
        info,
        warning,
    }
}
