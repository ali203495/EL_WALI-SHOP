<template>
    <div class="skeleton-card">
        <div class="skeleton-image skeleton"></div>
        <div class="skeleton-body">
            <div class="skeleton skeleton-brand"></div>
            <div class="skeleton skeleton-title"></div>
            <div class="skeleton skeleton-rating"></div>
            <div class="skeleton-footer">
                <div class="skeleton skeleton-price"></div>
                <div class="skeleton skeleton-button"></div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.skeleton-card {
    background: white;
    border-radius: var(--radius-lg);
    overflow: hidden;
    border: 1px solid var(--border);
}

.skeleton {
    background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
    background-size: 200% 100%;
    animation: shimmer 1.5s infinite;
    border-radius: 4px;
}

@keyframes shimmer {
    0% { background-position: 200% 0; }
    100% { background-position: -200% 0; }
}

.skeleton-image {
    height: 200px;
    background: #f0f0f0;
}

.skeleton-body {
    padding: 1.25rem;
}

.skeleton-brand {
    width: 60px;
    height: 12px;
    margin-bottom: 0.75rem;
}

.skeleton-title {
    width: 100%;
    height: 20px;
    margin-bottom: 0.5rem;
}

.skeleton-rating {
    width: 120px;
    height: 14px;
    margin-bottom: 1rem;
}

.skeleton-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.skeleton-price {
    width: 80px;
    height: 24px;
}

.skeleton-button {
    width: 100px;
    height: 32px;
    border-radius: var(--radius);
}
</style>
