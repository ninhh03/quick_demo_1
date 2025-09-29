<template>
  <div class="flex flex-col md:flex-row p-6 gap-6 bg-gray-50 min-h-screen">
    <!-- Sidebar Filter -->
    <aside class="w-full md:w-1/4">
      <div class="bg-white shadow rounded-xl p-4 sticky top-6">
        <h2 class="text-lg font-semibold mb-4">Bộ lọc</h2>


        <div class="mb-4">
          <label class="block text-sm font-medium mb-1">Tìm kiếm</label>
          <input v-model="search" type="text" placeholder="Nhập tên sản phẩm"
            class="w-full border px-3 py-2 rounded-lg focus:ring-2 focus:ring-blue-400" />
        </div>

        <!-- Địa chỉ -->
        <div class="mb-4">
          <label class="block text-sm font-medium mb-1">Theo địa chỉ</label>
          <select v-model="pendingFilters.diaChi"
            class="w-full border px-3 py-2 rounded-lg focus:ring-2 focus:ring-blue-400">
            <option value="">Chọn địa chỉ</option>
            <option value="Hà Nội">Hà Nội</option>
            <option value="Huế">Huế</option>
            <option value="Quảng Ninh">Quảng Ninh</option>
            <option value="Cao Bằng">Cao Bằng</option>
            <option value="Lạng Sơn">Lạng Sơn</option>
            <option value="Lai Châu">Lai Châu</option>
            <option value="Điện Biên">Điện Biên</option>
            <option value="Sơn La">Sơn La</option>
            <option value="Thanh Hóa">Thanh Hóa</option>
            <option value="Nghệ An">Nghệ An</option>
            <option value="Hà Tĩnh">Hà Tĩnh</option>
            <option value="Tuyên Quang">Tuyên Quang</option>
            <option value="Lào Cai">Lào Cai</option>
            <option value="Thái Nguyên">Thái Nguyên</option>
            <option value="Phú Thọ">Phú Thọ</option>
            <option value="Bắc Ninh">Bắc Ninh</option>
            <option value="Hưng Yên">Hưng Yên</option>
            <option value="Hải Phòng">Hải Phòng</option>
            <option value="Ninh Bình">Ninh Bình</option>
            <option value="Quảng Trị">Quảng Trị</option>
            <option value="Đà Nẵng">Đà Nẵng</option>
            <option value="Quảng Ngãi">Quảng Ngãi</option>
            <option value="Gia Lai">Gia Lai</option>
            <option value="Khánh Hòa">Khánh Hòa</option>
            <option value="Lâm Đồng">Lâm Đồng</option>
            <option value="Đắk Lắk">Đắk Lắk</option>
            <option value="Hồ Chí Minh">Hồ Chí Minh</option>
            <option value="Đồng Nai">Đồng Nai</option>
            <option value="Tây Ninh">Tây Ninh</option>
            <option value="Cần Thơ">Cần Thơ</option>
            <option value="Vĩnh Long">Vĩnh Long</option>
            <option value="Đồng Tháp">Đồng Tháp</option>
            <option value="Cà Mau">Cà Mau</option>
            <option value="An Giang">An Giang</option>
          </select>
        </div>

        <!-- Khoảng giá -->
<div class="mb-4 w-full">
  <label class="block text-sm font-medium mb-2">Khoảng giá (VNĐ)</label>

  <Slider
    v-model="pendingPriceRange"
    :min="0"
    :max="100000000000"
    :step="10000"
    :lazy="true"
    class="w-full mt-12"
  />

  <div class="flex gap-2 mt-4 w-full">
    <input
      v-model.number="pendingPriceRange[0]"
      type="number"
      placeholder="Giá thấp nhất"
      class="flex-1 border px-3 py-2 rounded-lg focus:ring-2 focus:ring-blue-400 w-full"
    />
    <input
      v-model.number="pendingPriceRange[1]"
      type="number"
      placeholder="Giá cao nhất"
      class="flex-1 border px-3 py-2 rounded-lg focus:ring-2 focus:ring-blue-400 w-full"
    />
  </div>


  <p class="text-sm text-gray-600 mt-4 w-full">
    {{ pendingPriceRange[0].toLocaleString() }} đ — {{ pendingPriceRange[1].toLocaleString() }} đ
  </p>
</div>




        <!-- Số lượng đánh giá -->
        <div class="mb-4">
          <label class="block text-sm font-medium mb-1">Số lượng đánh giá</label>
          <div class="flex gap-2">
            <input v-model.number="pendingFilters.minReviews" type="number" placeholder="Tối thiểu"
              class="w-1/2 border px-3 py-2 rounded-lg focus:ring-2 focus:ring-blue-400" />
            <input v-model.number="pendingFilters.maxReviews" type="number" placeholder="Tối đa"
              class="w-1/2 border px-3 py-2 rounded-lg focus:ring-2 focus:ring-blue-400" />
          </div>
        </div>

        <!-- Button apply -->
        <button @click="applyFilters"
          class="w-full bg-[#10B981] text-white py-2 rounded-lg hover:bg-[#0ea271] transition">
          Lọc
        </button>
      </div>
    </aside>


    <!-- Main content -->
    <main class="flex-1">


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
            <img
              :src="product.link_anh?.[0] || 'https://i0.wp.com/mikeyarce.com/wp-content/uploads/2021/09/woocommerce-placeholder.png?ssl=1'"
              alt="product image" class="w-full h-full object-cover hover:scale-110 transition duration-300" />
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
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { getProducts } from '~/services/api'
import Slider from '@vueform/slider'
import '@vueform/slider/themes/default.css'

const router = useRouter()
const route = useRoute()

/* ---------- config ---------- */
const limit = 9

/* ---------- reactive state ---------- */
const products = ref<any[]>([])
const page = ref(1)
const totalPages = ref(1)
const totalCount = ref(0)
const loading = ref(false)

const search = ref('')

/* filters thực sự dùng để gọi API */
const filters = ref({
  diaChi: '',
  minPrice: null as number | null,
  maxPrice: null as number | null,
  minReviews: null as number | null,
  maxReviews: null as number | null,
})

/* filters tạm (người dùng chỉnh) */
const pendingFilters = ref({ ...filters.value })
const priceRange = ref<[number, number]>([0, 50000000])
const pendingPriceRange = ref<[number, number]>([...priceRange.value])

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

/* ---------- Apply Filters ---------- */
const applyFilters = () => {
  filters.value = { ...pendingFilters.value }
  priceRange.value = [...pendingPriceRange.value]
  filters.value.minPrice = priceRange.value[0]
  filters.value.maxPrice = priceRange.value[1]

  page.value = 1
  loadProducts()
}

/* ---------- pagination ---------- */
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

/* computed */
const showPagination = computed(() => {
  return !loading.value && totalPages.value > 1
})

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

  /* đồng bộ pendingFilters với filters */
  pendingFilters.value = { ...filters.value }
  if (filters.value.minPrice != null && filters.value.maxPrice != null) {
    pendingPriceRange.value = [filters.value.minPrice, filters.value.maxPrice]
  }

  loadProducts()
})
</script>
