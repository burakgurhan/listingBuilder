import React, { useState } from 'react';
import { Wand2, Copy, Edit3, ChevronDown, ChevronUp, Loader2, ExternalLink } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';

interface GeneratedContent {
  titles: string[];
  description: string;
  bulletPoints: string[];
  keywordsReport: string;
}

function Dashboard() {
  const [url, setUrl] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedContent, setGeneratedContent] = useState<GeneratedContent | null>(null);
  const [showKeywords, setShowKeywords] = useState(false);
  const [editingDescription, setEditingDescription] = useState(false);
  const [editedDescription, setEditedDescription] = useState('');
  const { showToast } = useAuth();

  const handleGenerate = async () => {
    if (!url.trim()) {
      showToast('Please enter a valid URL', 'error');
      return;
    }

    // Basic URL validation
    try {
      new URL(url);
    } catch {
      showToast('Please enter a valid URL format', 'error');
      return;
    }

    setIsGenerating(true);
    setGeneratedContent(null); // Clear previous results
    try {
      // Backend integration point: POST /generate_text
      const response = await fetch('/api/v1/generate_text', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('authToken')}`,
        },
        body: JSON.stringify({ url }),
      });

      const data = await response.json();
      console.log('API response:', data); // Debug log
      if (!response.ok) {
        // Show backend error message if available
        showToast(data.detail || 'Failed to generate content', 'error');
        setIsGenerating(false);
        return;
      }
      // Check for empty or missing fields
      if (!data.titles?.length && !data.description && !data.bulletPoints?.length && !data.keywordsReport) {
        showToast('No content generated. Please try again with a different URL.', 'error');
        setIsGenerating(false);
        return;
      }
      setGeneratedContent(data);
      setEditedDescription(data.description);
      showToast('Content generated successfully!', 'success');
    } catch (error) {
      showToast('Failed to generate content. Please try again later.', 'error');
    } finally {
      setIsGenerating(false);
    }
  };

  const copyToClipboard = async (text: string, type: string) => {
    try {
      await navigator.clipboard.writeText(text);
      showToast(`${type} copied to clipboard!`, 'success');
    } catch (error) {
      showToast('Failed to copy to clipboard', 'error');
    }
  };

  const handleDescriptionEdit = () => {
    if (editingDescription) {
      setGeneratedContent(prev => prev ? {
        ...prev,
        description: editedDescription
      } : null);
      showToast('Description updated!', 'success');
    }
    setEditingDescription(!editingDescription);
  };

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="text-center mb-12">
        <div className="flex items-center justify-center mb-4">
          <Wand2 className="h-12 w-12 text-blue-600 mr-3" />
          <h1 className="text-4xl font-bold text-gray-900">AI-Powered Product Text Wizard</h1>
        </div>
        <p className="text-xl text-gray-600 max-w-3xl mx-auto">
          Transform any competitor product URL into compelling, SEO-optimized titles and descriptions that drive sales
        </p>
      </div>

      {/* Input Section */}
      <div className="bg-white rounded-2xl shadow-lg border border-gray-100 p-8 mb-8">
        <div className="max-w-4xl mx-auto">
          <label htmlFor="product-url" className="block text-lg font-semibold text-gray-900 mb-3">
            Enter Competitor Product URL
          </label>
          <div className="flex flex-col sm:flex-row gap-4">
            <div className="flex-1">
              <input
                type="url"
                id="product-url"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                placeholder="e.g., https://www.amazon.com/dp/B0BP7M5F3M"
                className="w-full px-4 py-4 text-lg border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors"
                disabled={isGenerating}
              />
            </div>
            <button
              onClick={handleGenerate}
              disabled={isGenerating || !url.trim()}
              className="px-8 py-4 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors whitespace-nowrap"
            >
              {isGenerating ? (
                <div className="flex items-center">
                  <Loader2 className="animate-spin h-5 w-5 mr-2" />
                  Generating...
                </div>
              ) : (
                <div className="flex items-center">
                  <Wand2 className="h-5 w-5 mr-2" />
                  Generate Text
                </div>
              )}
            </button>
          </div>
          
          {url && (
            <div className="mt-3 text-sm text-gray-500 flex items-center">
              <ExternalLink className="h-4 w-4 mr-1" />
              Analyzing: {url}
            </div>
          )}
        </div>
      </div>

      {/* Loading State */}
      {isGenerating && (
        <div className="bg-white rounded-2xl shadow-lg border border-gray-100 p-12 mb-8">
          <div className="text-center">
            <Loader2 className="animate-spin h-12 w-12 text-blue-600 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-gray-900 mb-2">AI is analyzing your product...</h3>
            <p className="text-gray-600">This may take a few moments while we generate optimized content</p>
            <div className="mt-6 bg-gray-200 rounded-full h-2 max-w-md mx-auto">
              <div className="bg-blue-600 h-2 rounded-full animate-pulse" style={{ width: '70%' }}></div>
            </div>
          </div>
        </div>
      )}

      {/* Results Section */}
      {generatedContent && !isGenerating && (
        <div className="space-y-8">
          {/* Product Titles */}
          <div className="bg-white rounded-2xl shadow-lg border border-gray-100 p-8">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-gray-900">Suggested Product Titles</h2>
              <button
                onClick={() => copyToClipboard(generatedContent.titles.join('\n'), 'All titles')}
                className="flex items-center px-4 py-2 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
              >
                <Copy className="h-4 w-4 mr-2" />
                Copy All
              </button>
            </div>
            <div className="space-y-4">
              {generatedContent.titles.map((title, index) => (
                <div key={index} className="group p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="text-sm text-blue-600 font-medium mb-1">Option {index + 1}</div>
                      <p className="text-gray-900 font-medium leading-relaxed">{title}</p>
                    </div>
                    <button
                      onClick={() => copyToClipboard(title, `Title ${index + 1}`)}
                      className="ml-4 opacity-0 group-hover:opacity-100 flex items-center px-3 py-1 text-blue-600 hover:bg-blue-100 rounded transition-all"
                    >
                      <Copy className="h-4 w-4 mr-1" />
                      Copy
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Product Description */}
          <div className="bg-white rounded-2xl shadow-lg border border-gray-100 p-8">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-gray-900">Suggested Product Description</h2>
              <div className="flex items-center space-x-3">
                <button
                  onClick={handleDescriptionEdit}
                  className="flex items-center px-4 py-2 text-gray-600 hover:bg-gray-50 rounded-lg transition-colors"
                >
                  <Edit3 className="h-4 w-4 mr-2" />
                  {editingDescription ? 'Save' : 'Edit'}
                </button>
                <button
                  onClick={() => copyToClipboard(generatedContent.description, 'Description')}
                  className="flex items-center px-4 py-2 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                >
                  <Copy className="h-4 w-4 mr-2" />
                  Copy
                </button>
              </div>
            </div>
            <div className="bg-gray-50 rounded-lg p-6">
              {editingDescription ? (
                <textarea
                  value={editedDescription}
                  onChange={(e) => setEditedDescription(e.target.value)}
                  className="w-full h-48 p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                />
              ) : (
                // Split description by double newlines and render as paragraphs
                generatedContent.description
                  .split(/\n\s*\n/)
                  .map((para, idx) => (
                    <p key={idx} className="text-gray-900 leading-relaxed text-lg mb-4 whitespace-pre-line">
                      {para}
                    </p>
                  ))
              )}
            </div>
          </div>

          {/* Bullet Points */}
          <div className="bg-white rounded-2xl shadow-lg border border-gray-100 p-8">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-gray-900">Key Feature Bullet Points</h2>
              <button
                onClick={() => copyToClipboard(generatedContent.bulletPoints.map(point => `• ${point}`).join('\n'), 'Bullet points')}
                className="flex items-center px-4 py-2 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
              >
                <Copy className="h-4 w-4 mr-2" />
                Copy All
              </button>
            </div>
            <div className="space-y-3">
              {generatedContent.bulletPoints.map((point, index) => (
                <div key={index} className="group flex items-start p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
                  <div className="flex-1 flex items-start">
                    <span className="text-blue-600 mr-2 mt-1">&#8226;</span>
                    <p className="text-gray-900 leading-relaxed">{point}</p>
                  </div>
                  <button
                    onClick={() => copyToClipboard(`• ${point}`, `Bullet point ${index + 1}`)}
                    className="ml-4 opacity-0 group-hover:opacity-100 flex items-center px-3 py-1 text-blue-600 hover:bg-blue-100 rounded transition-all"
                  >
                    <Copy className="h-4 w-4 mr-1" />
                    Copy
                  </button>
                </div>
              ))}
            </div>
          </div>

          {/* Keywords Report */}
          <div className="bg-white rounded-2xl shadow-lg border border-gray-100 p-8">
            <button
              onClick={() => setShowKeywords(!showKeywords)}
              className="flex items-center justify-between w-full text-left"
            >
              <h2 className="text-2xl font-bold text-gray-900">Keywords & SEO Report</h2>
              {showKeywords ? (
                <ChevronUp className="h-6 w-6 text-gray-500" />
              ) : (
                <ChevronDown className="h-6 w-6 text-gray-500" />
              )}
            </button>
            
            {showKeywords && (
              <div className="mt-6 p-6 bg-blue-50 rounded-lg border border-blue-100">
                {/* Split keywordsReport by newlines, commas, or semicolons and display each on a new line */}
                {generatedContent.keywordsReport
                  .split(/\n|,|;/)
                  .map((kw, idx) => {
                    const trimmed = kw.trim();
                    return trimmed ? (
                      <div key={idx} className="text-gray-800 leading-relaxed mb-1">{trimmed}</div>
                    ) : null;
                  })}
                <button
                  onClick={() => copyToClipboard(generatedContent.keywordsReport, 'Keywords report')}
                  className="mt-4 flex items-center px-4 py-2 text-blue-600 hover:bg-blue-100 rounded-lg transition-colors"
                >
                  <Copy className="h-4 w-4 mr-2" />
                  Copy Report
                </button>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default Dashboard;