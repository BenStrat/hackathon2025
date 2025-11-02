"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Video, Search, List, Info, CheckCircle2, XCircle, AlertCircle } from "lucide-react"

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

interface ParseResult {
  success: boolean
  url: string
  platform?: string
  video_id?: string
  caption?: string
  author?: string
  restaurant_found: boolean
  restaurant_name?: string
  confidence: number
  reasoning?: string
  additional_context?: string
  error?: string
}

export default function Home() {
  const [singleUrl, setSingleUrl] = useState("")
  const [batchUrls, setBatchUrls] = useState("")
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<ParseResult | null>(null)
  const [batchResults, setBatchResults] = useState<ParseResult[]>([])

  const parseSingleUrl = async () => {
    if (!singleUrl.trim()) return

    setLoading(true)
    setResult(null)

    try {
      const response = await fetch(`${API_URL}/parse`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ url: singleUrl }),
      })

      const data = await response.json()
      setResult(data)
    } catch (error) {
      setResult({
        success: false,
        url: singleUrl,
        restaurant_found: false,
        confidence: 0,
        error: "Failed to connect to API. Make sure the backend is running.",
      })
    } finally {
      setLoading(false)
    }
  }

  const parseBatchUrls = async () => {
    const urls = batchUrls.split("\n").filter((url) => url.trim())
    if (urls.length === 0) return

    setLoading(true)
    setBatchResults([])

    try {
      const response = await fetch(`${API_URL}/parse/batch`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ urls }),
      })

      const data = await response.json()
      setBatchResults(data)
    } catch (error) {
      setBatchResults([
        {
          success: false,
          url: "error",
          restaurant_found: false,
          confidence: 0,
          error: "Failed to connect to API. Make sure the backend is running.",
        },
      ])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800">
      <div className="container mx-auto px-4 py-8 max-w-7xl">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center mb-4">
            <Video className="w-12 h-12 text-blue-600 mr-3" />
            <h1 className="text-4xl font-bold text-gray-900 dark:text-white">
              Social Video Parser
            </h1>
          </div>
          <p className="text-lg text-gray-600 dark:text-gray-300">
            Parse TikTok & Instagram Reels • Extract Captions • Detect Restaurants with AI
          </p>
        </div>

        {/* Main Content */}
        <Tabs defaultValue="single" className="w-full">
          <TabsList className="grid w-full max-w-md mx-auto grid-cols-3">
            <TabsTrigger value="single">
              <Search className="w-4 h-4 mr-2" />
              Single URL
            </TabsTrigger>
            <TabsTrigger value="batch">
              <List className="w-4 h-4 mr-2" />
              Batch
            </TabsTrigger>
            <TabsTrigger value="about">
              <Info className="w-4 h-4 mr-2" />
              About
            </TabsTrigger>
          </TabsList>

          {/* Single URL Tab */}
          <TabsContent value="single" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>Parse Single Video URL</CardTitle>
                <CardDescription>
                  Enter a TikTok or Instagram Reels URL to analyze
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="url">Video URL</Label>
                  <div className="flex gap-2">
                    <Input
                      id="url"
                      placeholder="https://www.tiktok.com/@user/video/123 or https://www.instagram.com/reel/ABC/"
                      value={singleUrl}
                      onChange={(e) => setSingleUrl(e.target.value)}
                      onKeyPress={(e) => e.key === "Enter" && parseSingleUrl()}
                    />
                    <Button onClick={parseSingleUrl} disabled={loading}>
                      {loading ? "Parsing..." : "Parse"}
                    </Button>
                  </div>
                </div>

                {/* Results */}
                {result && (
                  <div className="mt-6 space-y-4">
                    {result.error ? (
                      <Card className="border-red-200 bg-red-50 dark:bg-red-900/20">
                        <CardContent className="pt-6">
                          <div className="flex items-start gap-3">
                            <XCircle className="w-5 h-5 text-red-600 mt-0.5" />
                            <div>
                              <p className="font-semibold text-red-900 dark:text-red-100">
                                Error
                              </p>
                              <p className="text-sm text-red-700 dark:text-red-200">
                                {result.error}
                              </p>
                            </div>
                          </div>
                        </CardContent>
                      </Card>
                    ) : (
                      <>
                        <Card>
                          <CardHeader>
                            <CardTitle className="text-lg">Video Information</CardTitle>
                          </CardHeader>
                          <CardContent className="space-y-3">
                            <div className="grid grid-cols-2 gap-4">
                              <div>
                                <p className="text-sm font-medium text-gray-500">Platform</p>
                                <p className="text-base font-semibold uppercase">
                                  {result.platform}
                                </p>
                              </div>
                              {result.author && (
                                <div>
                                  <p className="text-sm font-medium text-gray-500">Author</p>
                                  <p className="text-base font-semibold">@{result.author}</p>
                                </div>
                              )}
                            </div>
                            <div>
                              <p className="text-sm font-medium text-gray-500 mb-1">Caption</p>
                              <p className="text-sm bg-gray-50 dark:bg-gray-800 p-3 rounded-md">
                                {result.caption || "Caption not found"}
                              </p>
                            </div>
                          </CardContent>
                        </Card>

                        <Card>
                          <CardHeader>
                            <CardTitle className="text-lg flex items-center gap-2">
                              Restaurant Detection
                              {result.restaurant_found ? (
                                <CheckCircle2 className="w-5 h-5 text-green-600" />
                              ) : (
                                <XCircle className="w-5 h-5 text-gray-400" />
                              )}
                            </CardTitle>
                          </CardHeader>
                          <CardContent className="space-y-3">
                            <div className="grid grid-cols-2 gap-4">
                              <div>
                                <p className="text-sm font-medium text-gray-500">Restaurant Found</p>
                                <p className={`text-base font-semibold ${
                                  result.restaurant_found ? "text-green-600" : "text-gray-500"
                                }`}>
                                  {result.restaurant_found ? "Yes" : "No"}
                                </p>
                              </div>
                              {result.restaurant_found && result.restaurant_name && (
                                <div>
                                  <p className="text-sm font-medium text-gray-500">Restaurant Name</p>
                                  <p className="text-base font-semibold">{result.restaurant_name}</p>
                                </div>
                              )}
                            </div>
                            <div className="grid grid-cols-2 gap-4">
                              <div>
                                <p className="text-sm font-medium text-gray-500">Confidence</p>
                                <p className="text-base font-semibold">
                                  {(result.confidence * 100).toFixed(1)}%
                                </p>
                              </div>
                            </div>
                            {result.reasoning && (
                              <div>
                                <p className="text-sm font-medium text-gray-500 mb-1">Reasoning</p>
                                <p className="text-sm bg-gray-50 dark:bg-gray-800 p-3 rounded-md">
                                  {result.reasoning}
                                </p>
                              </div>
                            )}
                            {result.additional_context && (
                              <div>
                                <p className="text-sm font-medium text-gray-500 mb-1">
                                  Additional Context
                                </p>
                                <p className="text-sm bg-blue-50 dark:bg-blue-900/20 p-3 rounded-md">
                                  {result.additional_context}
                                </p>
                              </div>
                            )}
                          </CardContent>
                        </Card>
                      </>
                    )}
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          {/* Batch Processing Tab */}
          <TabsContent value="batch" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>Batch Process Multiple URLs</CardTitle>
                <CardDescription>
                  Enter multiple URLs (one per line) to analyze them all at once
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="batch-urls">Video URLs (one per line)</Label>
                  <Textarea
                    id="batch-urls"
                    placeholder="https://www.tiktok.com/@user/video/123&#10;https://www.instagram.com/reel/ABC/&#10;https://www.tiktok.com/@user2/video/456"
                    rows={8}
                    value={batchUrls}
                    onChange={(e) => setBatchUrls(e.target.value)}
                  />
                </div>
                <Button onClick={parseBatchUrls} disabled={loading} className="w-full">
                  {loading ? "Processing..." : "Parse All URLs"}
                </Button>

                {/* Batch Results */}
                {batchResults.length > 0 && (
                  <div className="mt-6 space-y-4">
                    <h3 className="text-lg font-semibold">
                      Results ({batchResults.length} {batchResults.length === 1 ? "URL" : "URLs"})
                    </h3>
                    {batchResults.map((result, index) => (
                      <Card key={index} className={result.error ? "border-red-200" : ""}>
                        <CardHeader>
                          <CardTitle className="text-base flex items-center gap-2">
                            {result.success ? (
                              <CheckCircle2 className="w-4 h-4 text-green-600" />
                            ) : (
                              <XCircle className="w-4 h-4 text-red-600" />
                            )}
                            {result.platform?.toUpperCase() || "Error"}
                          </CardTitle>
                          <CardDescription className="text-xs truncate">
                            {result.url}
                          </CardDescription>
                        </CardHeader>
                        <CardContent>
                          {result.error ? (
                            <p className="text-sm text-red-600">{result.error}</p>
                          ) : (
                            <div className="space-y-2 text-sm">
                              <div>
                                <span className="font-medium">Caption: </span>
                                <span className="text-gray-600 dark:text-gray-300">
                                  {result.caption?.substring(0, 100)}
                                  {result.caption && result.caption.length > 100 ? "..." : ""}
                                </span>
                              </div>
                              <div className="flex items-center gap-4">
                                <div>
                                  <span className="font-medium">Restaurant: </span>
                                  <span className={result.restaurant_found ? "text-green-600" : "text-gray-500"}>
                                    {result.restaurant_found ? result.restaurant_name : "Not found"}
                                  </span>
                                </div>
                                <div>
                                  <span className="font-medium">Confidence: </span>
                                  <span>{(result.confidence * 100).toFixed(1)}%</span>
                                </div>
                              </div>
                            </div>
                          )}
                        </CardContent>
                      </Card>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          {/* About Tab */}
          <TabsContent value="about">
            <Card>
              <CardHeader>
                <CardTitle>About Social Video Parser</CardTitle>
                <CardDescription>
                  AI-powered tool to extract insights from social media videos
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4 text-sm">
                <div>
                  <h3 className="font-semibold mb-2">Features</h3>
                  <ul className="list-disc list-inside space-y-1 text-gray-600 dark:text-gray-300">
                    <li>Parse TikTok and Instagram Reels URLs</li>
                    <li>Extract video captions and descriptions</li>
                    <li>AI-powered restaurant detection</li>
                    <li>Batch processing for multiple URLs</li>
                    <li>Confidence scores and detailed reasoning</li>
                  </ul>
                </div>

                <div>
                  <h3 className="font-semibold mb-2">Supported Platforms</h3>
                  <div className="space-y-2 text-gray-600 dark:text-gray-300">
                    <div>
                      <p className="font-medium">TikTok</p>
                      <p className="text-xs">Standard URLs, short links (vm.tiktok.com), mobile links</p>
                    </div>
                    <div>
                      <p className="font-medium">Instagram</p>
                      <p className="text-xs">Reels, posts, and IGTV videos</p>
                    </div>
                  </div>
                </div>

                <div>
                  <h3 className="font-semibold mb-2">How It Works</h3>
                  <ol className="list-decimal list-inside space-y-1 text-gray-600 dark:text-gray-300">
                    <li>Paste a video URL from TikTok or Instagram</li>
                    <li>The system extracts the video caption using web scraping</li>
                    <li>AI analyzes the caption to detect restaurant mentions</li>
                    <li>Results include confidence scores and reasoning</li>
                  </ol>
                </div>

                <div className="pt-4 border-t">
                  <p className="text-xs text-gray-500 text-center">
                    Built with Next.js, shadcn/ui, FastAPI, and OpenAI
                  </p>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}
