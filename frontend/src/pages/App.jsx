import './App.css'

const products = [
  {
    id: 1,
    name: 'Книжная полка',
    type: 'bookshelf',
    price: 8500,
    description: 'Стеллаж для книг с тремя полками',
    dimensions: '800 × 400 × 1200 мм',
    image: 'https://placehold.co/400x300/e8e8e8/999999?text=Книжная+полка'
  },
  {
    id: 2,
    name: 'Прикроватная тумба',
    type: 'nightstand',
    price: 5200,
    description: 'Компактная тумба с ящиком',
    dimensions: '450 × 400 × 500 мм',
    image: 'https://placehold.co/400x300/e8e8e8/999999?text=Тумба'
  },
  {
    id: 3,
    name: 'Комод',
    type: 'dresser',
    price: 12500,
    description: 'Комод с четырьмя ящиками',
    dimensions: '1200 × 450 × 800 мм',
    image: 'https://placehold.co/400x300/e8e8e8/999999?text=Комод'
  }
]

function App() {
  return (
    <div className="app">
      <header className="header">
        <div className="container">
          <h1 className="logo">Yartumba</h1>
          <nav className="nav">
            <a href="#" className="nav-link active">Каталог</a>
            <a href="#" className="nav-link">Контакты</a>
          </nav>
        </div>
      </header>

      <main className="main">
        <div className="container">
          <h2 className="page-title">Каталог мебели</h2>
          
          <div className="products-grid">
            {products.map(product => (
              <article key={product.id} className="product-card">
                <div className="product-image">
                  <img src={product.image} alt={product.name} />
                </div>
                <div className="product-info">
                  <h3 className="product-name">{product.name}</h3>
                  <p className="product-description">{product.description}</p>
                  <p className="product-dimensions">{product.dimensions}</p>
                  <div className="product-footer">
                    <span className="product-price">{product.price.toLocaleString()} ₽</span>
                    <button className="btn btn-primary">Подробнее</button>
                  </div>
                </div>
              </article>
            ))}
          </div>
        </div>
      </main>

      <footer className="footer">
        <div className="container">
          <p>© 2024 Yartumba — Мебель на заказ</p>
        </div>
      </footer>
    </div>
  )
}

export default App
