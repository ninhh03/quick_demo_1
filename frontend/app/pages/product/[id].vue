<template>
  <div class="p-6 bg-gray-50 min-h-screen">
    <!-- Loading -->
    <div v-if="loading" class="text-center py-10 text-gray-500">
      Đang tải dữ liệu...
    </div>

    <!-- Error -->
    <div v-else-if="error" class="text-center py-10 text-red-500">
      {{ error }}
    </div>

    <!-- Product -->
    <div v-else class="max-w-5xl mx-auto bg-white rounded-xl shadow-lg p-6">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Ảnh chính + thumbnails -->
        <div>
          <img
            :src="product.images[0] || placeholder"
            alt="Product image"
            class="rounded-xl w-full h-96 object-cover mb-4"
          />
          <div class="flex gap-3">
            <img
              v-for="(img, index) in product.images"
              :key="index"
              :src="img"
              class="w-20 h-20 rounded-lg border cursor-pointer object-cover hover:scale-105 transition"
              @click="setMainImage(img)"
            />
          </div>
        </div>

        <!-- Thông tin sản phẩm -->
        <div>
          <h1 class="text-2xl font-bold mb-2">{{ product.name }}</h1>
          <p class="text-xl text-red-500 font-semibold mb-4">{{ product.price }}</p>
          <p class="text-gray-600 mb-2">
            <span class="font-medium">Địa chỉ:</span> {{ product.address }}
          </p>
          <p class="text-gray-600 mb-2">
            <span class="font-medium">Đánh giá:</span> {{ product.rating }}
          </p>
          <button
            class="mt-4 bg-blue-600 text-white px-4 py-2 rounded-xl shadow hover:bg-blue-700 transition"
          >
            Mua ngay
          </button>
        </div>
      </div>

      <!-- Mô tả -->
      <div class="mt-8">
        <h2 class="text-lg font-semibold mb-3">Mô tả sản phẩm</h2>
        <p class="text-gray-700 leading-relaxed">{{ product.description }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getProductById } from '~/services/api'

const route = useRoute()
const productId = route.params.id as string

// Khởi tạo product với cấu trúc chuẩn
const product = ref({
  id: '',
  name: '',
  price: '',
  address: '',
  rating: 0,
  description: '',
  images: [] as string[],
})
const loading = ref(true)
const error = ref('')
const placeholder = ref('https://i0.wp.com/mikeyarce.com/wp-content/uploads/2021/09/woocommerce-placeholder.png?ssl=1')

// Load product từ API
const loadProduct = async () => {
  loading.value = true
  error.value = ''
  try {
    const res = await getProductById(productId)
    if (!res || res.error) {
      error.value = res?.error || 'Sản phẩm không tồn tại.'
      return
    }

    // Map dữ liệu từ API sang format frontend
    product.value = {
      id: res.id,
      name: res.ten_san_pham || '',
      price: res.gia || '',
      address: res.dia_chi || '',
      rating: res.so_luong_danh_gia ?? 0,
      description: res.mo_ta || '',
      images: res.link_anh ?? [],
    }
  } catch (err) {
    console.error('Failed to load product', err)
    error.value = 'Không tải được sản phẩm.'
  } finally {
    loading.value = false
  }
}

// Chọn ảnh chính khi click thumbnail
function setMainImage(img: string) {
  const imgs = product.value.images
  const index = imgs.indexOf(img)
  if (index > -1) {
    imgs.splice(index, 1)
    imgs.unshift(img)
  }
}

onMounted(() => loadProduct())
</script>
