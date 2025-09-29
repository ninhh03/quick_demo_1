<template>
  <div class="flex flex-col md:flex-row p-6 gap-6 bg-gray-50 min-h-screen">
    <!-- Sidebar Filter -->
    <aside class="w-full md:w-1/4">
      <div class="bg-white shadow rounded-xl p-4 sticky top-6">
        <h2 class="text-lg font-semibold mb-4">Bộ lọc</h2>

        <!-- Địa chỉ -->
        <div class="mb-4">
          <label class="block text-sm font-medium mb-1">Theo địa chỉ</label>
          <input v-model="filters.diaChi" type="text" placeholder="Nhập địa chỉ..."
            class="w-full border px-3 py-2 rounded-lg focus:ring-2 focus:ring-blue-400" />
        </div>

        <!-- Khoảng giá -->
        <div class="mb-4">
          <label class="block text-sm font-medium mb-1">Khoảng giá</label>
          <div class="flex gap-2">
            <input v-model.number="filters.minPrice" type="number" placeholder="Từ"
              class="w-1/2 border px-3 py-2 rounded-lg focus:ring-2 focus:ring-blue-400" />
            <input v-model.number="filters.maxPrice" type="number" placeholder="Đến"
              class="w-1/2 border px-3 py-2 rounded-lg focus:ring-2 focus:ring-blue-400" />
          </div>
        </div>

        <!-- Số lượng đánh giá -->
        <div class="mb-4">
          <label class="block text-sm font-medium mb-1">Số lượng đánh giá</label>
          <div class="flex gap-2">
            <input v-model.number="filters.minReviews" type="number" placeholder="Tối thiểu"
              class="w-1/2 border px-3 py-2 rounded-lg focus:ring-2 focus:ring-blue-400" />
            <input v-model.number="filters.maxReviews" type="number" placeholder="Tối đa"
              class="w-1/2 border px-3 py-2 rounded-lg focus:ring-2 focus:ring-blue-400" />
          </div>
        </div>


      </div>
    </aside>

    <!-- Main content -->
    <main class="flex-1">
      <!-- Search -->
      <div class="mb-6">
        <div class="flex items-center bg-white shadow rounded-xl overflow-hidden">
          <input v-model="search" type="text" placeholder="Tìm kiếm"
            class="flex-1 px-4 py-3 outline-none" />

        </div>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="text-center py-10 text-gray-500">
        Đang tải dữ liệu...
      </div>

      <!-- Empty state -->
      <div v-else-if="products.length === 0" class="text-center py-10 text-gray-500">
        Không có sản phẩm nào phù hợp.
      </div>

      <!-- Danh sách sản phẩm -->
      <ul v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        <li v-for="product in products" :key="product.id"
          class="bg-white rounded-2xl shadow hover:shadow-lg cursor-pointer overflow-hidden transition transform hover:-translate-y-1"
          @click="goToDetail(product.id)">
          <div class="overflow-hidden h-48">
            <img :src="product.link_anh?.[0] || 'https://i0.wp.com/mikeyarce.com/wp-content/uploads/2021/09/woocommerce-placeholder.png?ssl=1'" alt="product image"
              class="w-full h-full object-cover hover:scale-110 transition duration-300" />
          </div>
          <div class="p-4 space-y-1">
            <p class="font-semibold text-gray-800 line-clamp-1">
              {{ product.ten_san_pham }}
            </p>
            <p class="text-blue-600 font-medium">
              {{ product.gia || 'Chưa có giá' }}
            </p>
            <p class="text-gray-500 text-sm line-clamp-1">
              {{ product.dia_chi || 'Chưa có địa chỉ' }}
            </p>
          </div>
        </li>
      </ul>


      <!-- Pagination -->
      <div v-if="showPagination" class="flex flex-col items-center gap-3 mt-8">
        <div class="flex justify-center gap-2 items-center flex-wrap">
          <!-- Prev -->
          <button @click="prevPage" :disabled="page === 1" :class="[
            'px-3 py-1 rounded-lg',
            page === 1
              ? 'bg-gray-200 opacity-60 cursor-not-allowed'
              : 'bg-gray-200 hover:bg-gray-300'
          ]">
            Prev
          </button>

          <!-- Page numbers -->
          <button v-for="p in visiblePages" :key="p" @click="goToPage(p)" :class="[
            'px-3 py-1 rounded-lg',
            page === p
              ? 'bg-blue-600 text-white'
              : 'bg-gray-100 hover:bg-gray-200'
          ]">
            {{ p }}
          </button>

          <!-- Next -->
          <button @click="nextPage" :disabled="page >= totalPages" :class="[
            'px-3 py-1 rounded-lg',
            page >= totalPages
              ? 'bg-gray-200 opacity-60 cursor-not-allowed'
              : 'bg-gray-200 hover:bg-gray-300'
          ]">
            Next
          </button>
        </div>

        <p class="text-sm text-gray-500 mt-2">
          Tổng: {{ totalCount }} sản phẩm
        </p>
      </div>


    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { getProducts } from '~/services/api'

const router = useRouter()
const route = useRoute()

/* ---------- config ---------- */
const limit = 9
const debounceMs = 500

/* ---------- reactive state ---------- */
const products = ref<any[]>([])
const page = ref(1)
const totalPages = ref(1)
const totalCount = ref(0)
const loading = ref(false)

const search = ref('')
const filters = ref({
  diaChi: '',
  minPrice: null as number | null,
  maxPrice: null as number | null,
  minReviews: null as number | null,
  maxReviews: null as number | null,
})

onMounted(() => {
  document.title = "Chợ Tốt"
})

/* ---------- helpers ---------- */
const parsePagination = (payload: any) => {
  const pagination = payload?.pagination ?? payload?.meta ?? payload?.pageMeta ?? {}
  const total =
    payload?.totalCount ??
    pagination?.total ??
    payload?.total ??
    payload?.count ??
    (Array.isArray(payload?.data) ? payload.data.length : undefined)

  const totalPagesFromPayload =
    payload?.totalPages ??
    pagination?.totalPages ??
    (total ? Math.max(1, Math.ceil(total / limit)) : undefined)

  return {
    total: typeof total === 'number' ? total : 0,
    totalPages: typeof totalPagesFromPayload === 'number' ? totalPagesFromPayload : 1,
  }
}

/* ---------- API call ---------- */
const loadProducts = async () => {
  loading.value = true
  try {
    const params: any = {
      page: page.value,
      limit,
      ...(search.value ? { search: search.value } : {}),
      ...(filters.value.diaChi ? { diaChi: filters.value.diaChi } : {}),
      ...(filters.value.minPrice != null ? { minPrice: filters.value.minPrice } : {}),
      ...(filters.value.maxPrice != null ? { maxPrice: filters.value.maxPrice } : {}),
      ...(filters.value.minReviews != null ? { minReviews: filters.value.minReviews } : {}),
      ...(filters.value.maxReviews != null ? { maxReviews: filters.value.maxReviews } : {}),
      
    }

    const res = await getProducts(params)


    const items = res?.data ?? res?.items ?? res?.rows ?? []
    products.value = Array.isArray(items) ? items : []

    const { total, totalPages: tp } = parsePagination(res ?? {})
    totalCount.value = total || items.length
    totalPages.value = tp || Math.max(1, Math.ceil(totalCount.value / limit))


    router.replace({
  query: {
    page: String(page.value),
    search: search.value || undefined,
    diaChi: filters.value.diaChi || undefined,
    minPrice: filters.value.minPrice?.toString(),
    maxPrice: filters.value.maxPrice?.toString(),
    minReviews: filters.value.minReviews?.toString(),
    maxReviews: filters.value.maxReviews?.toString(),
  },
})

  } catch (err) {
    console.error('Failed to load products', err)
    products.value = []
    totalPages.value = 1
    totalCount.value = 0
  } finally {
    loading.value = false
  }
}

/* ---------- pagination ---------- */
const applyFilters = () => {
  page.value = 1
  loadProducts()
}

const nextPage = () => {
  if (page.value < totalPages.value) {
    page.value++
    loadProducts()
  }
}
const prevPage = () => {
  if (page.value > 1) {
    page.value--
    loadProducts()
  }
}
const goToPage = (p: number) => {
  if (p !== page.value) {
    page.value = p
    loadProducts()
  }
}

/* visible page numbers (max 6) */
const visiblePages = computed(() => {
  const max = 6
  let start = Math.max(1, page.value - Math.floor(max / 2))
  let end = start + max - 1

  if (end > totalPages.value) {
    end = totalPages.value
    start = Math.max(1, end - max + 1)
  }

  return Array.from({ length: end - start + 1 }, (_, i) => start + i)
})

/* watchers */
watch(
  () => [search.value, JSON.stringify(filters.value)],
  () => {
    if (debounceTimer) clearTimeout(debounceTimer)
    debounceTimer = setTimeout(() => {
      page.value = 1
      loadProducts()
      debounceTimer = null
    }, debounceMs)
  }
)

/* computed */
const showPagination = computed(() => {
  return !loading.value && totalPages.value > 1
})

/* debounce timer */
let debounceTimer: ReturnType<typeof setTimeout> | null = null

/* navigation */
const goToDetail = (id: string) => {
  router.push(`/product/${id}`)
}

/* init */
onMounted(() => {
  const q = route.query

  const pageParam = parseInt(q.page as string)
  if (!isNaN(pageParam) && pageParam > 0) {
    page.value = pageParam
  }

  if (q.search) search.value = q.search as string
  if (q.diaChi) filters.value.diaChi = q.diaChi as string
  if (q.minPrice) filters.value.minPrice = parseFloat(q.minPrice as string)
  if (q.maxPrice) filters.value.maxPrice = parseFloat(q.maxPrice as string)
  if (q.minReviews) filters.value.minReviews = parseInt(q.minReviews as string)
  if (q.maxReviews) filters.value.maxReviews = parseInt(q.maxReviews as string)

  loadProducts()
})

</script>
