import React from 'react';
import { BookOpen, Clock, User, ArrowRight } from 'lucide-react';

function Blogs() {
  const blogPosts = [
    {
      id: 1,
      title: '10 Proven Strategies to Boost Your E-commerce Conversion Rate',
      excerpt: 'Learn how to optimize your product pages and descriptions to convert more visitors into customers.',
      author: 'Sarah Johnson',
      date: '2024-01-15',
      readTime: '5 min read',
      image: 'https://images.pexels.com/photos/230544/pexels-photo-230544.jpeg?auto=compress&cs=tinysrgb&w=800',
      category: 'Conversion Optimization'
    },
    {
      id: 2,
      title: 'The Ultimate Guide to SEO-Optimized Product Descriptions',
      excerpt: 'Master the art of writing product descriptions that rank well in search engines and drive sales.',
      author: 'Mike Chen',
      date: '2024-01-12',
      readTime: '8 min read',
      image: 'https://images.pexels.com/photos/267350/pexels-photo-267350.jpeg?auto=compress&cs=tinysrgb&w=800',
      category: 'SEO'
    },
    {
      id: 3,
      title: 'How AI is Revolutionizing E-commerce Content Creation',
      excerpt: 'Discover how artificial intelligence is changing the way online sellers create product content.',
      author: 'Emily Rodriguez',
      date: '2024-01-10',
      readTime: '6 min read',
      image: 'https://images.pexels.com/photos/373543/pexels-photo-373543.jpeg?auto=compress&cs=tinysrgb&w=800',
      category: 'AI & Technology'
    },
    {
      id: 4,
      title: 'Amazon Listing Optimization: A Complete Guide for 2024',
      excerpt: 'Step-by-step guide to optimizing your Amazon product listings for maximum visibility and sales.',
      author: 'David Park',
      date: '2024-01-08',
      readTime: '10 min read',
      image: 'https://images.pexels.com/photos/4968630/pexels-photo-4968630.jpeg?auto=compress&cs=tinysrgb&w=800',
      category: 'Amazon'
    },
    {
      id: 5,
      title: 'Psychology of Product Titles: What Makes Customers Click',
      excerpt: 'Understand the psychological triggers that make product titles irresistible to potential buyers.',
      author: 'Lisa Thompson',
      date: '2024-01-05',
      readTime: '7 min read',
      image: 'https://images.pexels.com/photos/590020/pexels-photo-590020.jpeg?auto=compress&cs=tinysrgb&w=800',
      category: 'Psychology'
    },
    {
      id: 6,
      title: 'Competitor Analysis for E-commerce: Tools and Techniques',
      excerpt: 'Learn how to analyze your competitors and use insights to improve your own product listings.',
      author: 'Robert Kim',
      date: '2024-01-03',
      readTime: '9 min read',
      image: 'https://images.pexels.com/photos/669610/pexels-photo-669610.jpeg?auto=compress&cs=tinysrgb&w=800',
      category: 'Strategy'
    }
  ];

  const categories = ['All', 'SEO', 'Conversion Optimization', 'AI & Technology', 'Amazon', 'Psychology', 'Strategy'];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="flex items-center mb-8">
        <BookOpen className="h-8 w-8 text-blue-600 mr-3" />
        <h1 className="text-3xl font-bold text-gray-900">E-commerce Insights & Tips</h1>
      </div>

      <div className="mb-8">
        <p className="text-lg text-gray-600 mb-6">
          Stay updated with the latest strategies, tips, and insights to boost your e-commerce success.
        </p>
        
        {/* Category Filter */}
        <div className="flex flex-wrap gap-2">
          {categories.map((category) => (
            <button
              key={category}
              className="px-4 py-2 rounded-full text-sm font-medium border border-gray-300 hover:bg-blue-50 hover:border-blue-300 hover:text-blue-700 transition-colors"
            >
              {category}
            </button>
          ))}
        </div>
      </div>

      {/* Featured Article */}
      <div className="bg-gradient-to-r from-blue-600 to-cyan-600 rounded-2xl p-8 mb-12 text-white">
        <div className="grid lg:grid-cols-2 gap-8 items-center">
          <div>
            <div className="inline-block px-3 py-1 bg-white/20 rounded-full text-sm font-medium mb-4">
              Featured Article
            </div>
            <h2 className="text-3xl font-bold mb-4">
              The Complete Guide to AI-Powered Product Content
            </h2>
            <p className="text-blue-100 mb-6 text-lg">
              Learn how to leverage artificial intelligence to create compelling product content that converts and ranks higher in search results.
            </p>
            <button className="flex items-center bg-white text-blue-600 px-6 py-3 rounded-lg font-semibold hover:bg-blue-50 transition-colors">
              Read Full Article
              <ArrowRight className="ml-2 h-5 w-5" />
            </button>
          </div>
          <div className="hidden lg:block">
            <img
              src="https://images.pexels.com/photos/3184292/pexels-photo-3184292.jpeg?auto=compress&cs=tinysrgb&w=800"
              alt="AI Content Creation"
              className="rounded-xl shadow-lg"
            />
          </div>
        </div>
      </div>

      {/* Blog Posts Grid */}
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
        {blogPosts.map((post) => (
          <article
            key={post.id}
            className="bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden hover:shadow-xl transition-shadow group"
          >
            <div className="relative overflow-hidden">
              <img
                src={post.image}
                alt={post.title}
                className="w-full h-48 object-cover group-hover:scale-105 transition-transform duration-300"
              />
              <div className="absolute top-4 left-4">
                <span className="px-3 py-1 bg-blue-600 text-white text-xs font-medium rounded-full">
                  {post.category}
                </span>
              </div>
            </div>
            
            <div className="p-6">
              <h3 className="text-xl font-bold text-gray-900 mb-3 line-clamp-2 group-hover:text-blue-600 transition-colors">
                {post.title}
              </h3>
              <p className="text-gray-600 mb-4 line-clamp-3">{post.excerpt}</p>
              
              <div className="flex items-center justify-between text-sm text-gray-500 mb-4">
                <div className="flex items-center">
                  <User className="h-4 w-4 mr-1" />
                  {post.author}
                </div>
                <div className="flex items-center">
                  <Clock className="h-4 w-4 mr-1" />
                  {post.readTime}
                </div>
              </div>
              
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-500">{new Date(post.date).toLocaleDateString()}</span>
                <button className="flex items-center text-blue-600 font-medium hover:text-blue-700 transition-colors">
                  Read More
                  <ArrowRight className="ml-1 h-4 w-4" />
                </button>
              </div>
            </div>
          </article>
        ))}
      </div>

      {/* Newsletter Signup */}
      <div className="mt-16 bg-gray-900 rounded-2xl p-8 text-center">
        <h2 className="text-2xl font-bold text-white mb-4">Stay Updated</h2>
        <p className="text-gray-300 mb-6 max-w-2xl mx-auto">
          Get the latest e-commerce tips, strategies, and insights delivered straight to your inbox.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 max-w-md mx-auto">
          <input
            type="email"
            placeholder="Enter your email"
            className="flex-1 px-4 py-3 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none"
          />
          <button className="px-6 py-3 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition-colors">
            Subscribe
          </button>
        </div>
      </div>
    </div>
  );
}

export default Blogs;