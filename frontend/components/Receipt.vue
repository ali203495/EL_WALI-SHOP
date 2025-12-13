<script setup lang="ts">
interface ReceiptItem {
    name: string
    quantity: number
    price: number
}

defineProps<{
    orderId: number
    items: ReceiptItem[]
    subtotal: number
    tax: number
    total: number
    date?: string
}>()

const printReceipt = () => {
    window.print()
}
</script>

<template>
    <div class="receipt">
        <div class="receipt-header">
            <h2>MAISON EL WALI</h2>
            <p>Luxury Gold & Jewelry</p>
        </div>
        
        <div class="receipt-meta">
            <p>Order #{{ orderId.toString().padStart(4, '0') }}</p>
            <p>{{ date || new Date().toLocaleString() }}</p>
        </div>
        
        <div class="receipt-divider">- - - - - - - - - - - - - - - - -</div>
        
        <div class="receipt-items">
            <div v-for="item in items" :key="item.name" class="receipt-item">
                <div class="item-details">
                    <span class="item-name">{{ item.name }}</span>
                    <span class="item-qty">x{{ item.quantity }}</span>
                </div>
                <span class="item-price">${{ (item.price * item.quantity).toFixed(2) }}</span>
            </div>
        </div>
        
        <div class="receipt-divider">- - - - - - - - - - - - - - - - -</div>
        
        <div class="receipt-totals">
            <div class="total-row">
                <span>Subtotal</span>
                <span>${{ subtotal.toFixed(2) }}</span>
            </div>
            <div class="total-row">
                <span>Tax (8%)</span>
                <span>${{ tax.toFixed(2) }}</span>
            </div>
            <div class="total-row total-final">
                <span>TOTAL</span>
                <span>${{ total.toFixed(2) }}</span>
            </div>
        </div>
        
        <div class="receipt-divider">- - - - - - - - - - - - - - - - -</div>
        
        <div class="receipt-footer">
            <p>Thank you for your purchase!</p>
            <p class="small">Keep this receipt for your records</p>
        </div>
        
        <button class="print-btn" @click="printReceipt">🖨️ Print Receipt</button>
    </div>
</template>

<style scoped>
.receipt {
    background: white;
    padding: 2rem;
    font-family: 'Courier New', monospace; /* Invoice style */
    max-width: 320px;
    margin: 0 auto;
}

.receipt-header {
    text-align: center;
    margin-bottom: 1.5rem;
}

.receipt-header h2 {
    font-size: 1.25rem;
    margin-bottom: 0.25rem;
}

.receipt-header p {
    font-size: 0.75rem;
    color: var(--text-muted);
}

.receipt-meta {
    text-align: center;
    font-size: 0.8125rem;
    color: var(--text-muted);
    margin-bottom: 1rem;
}

.receipt-divider {
    text-align: center;
    color: #cbd5e1;
    margin: 1rem 0;
    font-size: 0.75rem;
}

.receipt-items {
    margin: 1rem 0;
}

.receipt-item {
    display: flex;
    justify-content: space-between;
    margin-bottom: 0.5rem;
    font-size: 0.8125rem;
}

.item-details {
    display: flex;
    gap: 0.5rem;
}

.item-qty {
    color: var(--text-muted);
}

.receipt-totals {
    margin: 1rem 0;
}

.total-row {
    display: flex;
    justify-content: space-between;
    font-size: 0.875rem;
    margin-bottom: 0.5rem;
}

.total-final {
    font-size: 1.125rem;
    font-weight: 700;
    margin-top: 0.75rem;
    padding-top: 0.75rem;
    border-top: 2px solid var(--text);
}

.receipt-footer {
    text-align: center;
    margin-top: 1.5rem;
}

.receipt-footer p {
    font-size: 0.8125rem;
}

.receipt-footer .small {
    font-size: 0.6875rem;
    color: var(--text-muted);
    margin-top: 0.25rem;
}

.print-btn {
    width: 100%;
    margin-top: 1.5rem;
    padding: 0.75rem;
    background: #0f172a;
    color: white;
    border: none;
    border-radius: var(--radius);
    font-family: inherit;
    cursor: pointer;
}

.print-btn:hover {
    background: #1e293b;
}

@media print {
    .print-btn {
        display: none;
    }
}
</style>
