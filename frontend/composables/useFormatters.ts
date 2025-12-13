export const useFormatters = () => {
    const formatPrice = (price: number): string => {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD',
            minimumFractionDigits: 0,
            maximumFractionDigits: 2,
        }).format(price)
    }

    const formatNumber = (num: number): string => {
        return new Intl.NumberFormat('en-US').format(num)
    }

    const formatCompact = (num: number): string => {
        return new Intl.NumberFormat('en-US', {
            notation: 'compact',
            maximumFractionDigits: 1,
        }).format(num)
    }

    const formatDate = (date: string | Date): string => {
        return new Intl.DateTimeFormat('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
        }).format(new Date(date))
    }

    return {
        formatPrice,
        formatNumber,
        formatCompact,
        formatDate,
    }
}
