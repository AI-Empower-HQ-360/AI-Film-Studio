"use client";

/**
 * @label Subtitle Generator Page
 * @description Next.js page for generating, translating, and burning subtitles
 */

import { useState, useEffect } from "react";
import { api } from "@/lib/api";
// Note: UI components should be created or imported from your component library
// For now, using basic HTML elements with Tailwind classes
// You may need to create these components or install shadcn/ui
import { Tabs, TabsContent, TabsList, TabsTrigger } from "../../components/ui/tabs";
import { Loader2, CheckCircle2, XCircle, FileText, Languages, Video } from "lucide-react";

export default function SubtitleGeneratorPage() {
  const [activeTab, setActiveTab] = useState("generate");
  
  // Generate subtitles state
  const [audioUrl, setAudioUrl] = useState("");
  const [modelName, setModelName] = useState("whisper-large-v3");
  const [sourceLanguage, setSourceLanguage] = useState("en");
  const [outputFormat, setOutputFormat] = useState("srt");
  const [speakerDiarization, setSpeakerDiarization] = useState(false);
  const [maxLineLength, setMaxLineLength] = useState(42);
  const [multiLanguages, setMultiLanguages] = useState<string[]>([]);
  const [selectedLanguage, setSelectedLanguage] = useState("en");
  
  // Translate subtitles state
  const [subtitleUrl, setSubtitleUrl] = useState("");
  const [targetLanguages, setTargetLanguages] = useState<string[]>([]);
  const [translationService, setTranslationService] = useState("google-translate");
  const [preserveTiming, setPreserveTiming] = useState(true);
  
  // Burn subtitles state
  const [videoUrl, setVideoUrl] = useState("");
  const [burnSubtitleUrl, setBurnSubtitleUrl] = useState("");
  const [fontName, setFontName] = useState("Arial");
  const [fontSize, setFontSize] = useState(24);
  const [fontColor, setFontColor] = useState("white");
  const [backgroundColor, setBackgroundColor] = useState("black");
  const [position, setPosition] = useState("bottom");
  
  // Common state
  const [supportedLanguages, setSupportedLanguages] = useState<string[]>([]);
  const [supportedFormats, setSupportedFormats] = useState<string[]>([]);
  const [translationServices, setTranslationServices] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [jobId, setJobId] = useState<string | null>(null);
  const [jobStatus, setJobStatus] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<any>(null);

  useEffect(() => {
    loadSupportedOptions();
  }, []);

  const loadSupportedOptions = async () => {
    try {
      const [languages, formats, services] = await Promise.all([
        api.request<{ languages: string[] }>("/api/v1/subtitles/languages"),
        api.request<{ formats: string[] }>("/api/v1/subtitles/formats"),
        api.request<{ services: any[] }>("/api/v1/subtitles/translation-services")
      ]);
      
      setSupportedLanguages(languages.languages || []);
      setSupportedFormats(formats.formats || []);
      setTranslationServices(services.services || []);
    } catch (err) {
      console.error("Failed to load supported options:", err);
    }
  };

  const handleGenerateSubtitles = async () => {
    if (!audioUrl.trim()) {
      setError("Please enter an audio URL");
      return;
    }

    setError(null);
    setLoading(true);
    setJobId(null);
    setJobStatus(null);
    setResult(null);

    try {
      const requestBody: any = {
        audio_url: audioUrl,
        model_name: modelName,
        source_language: sourceLanguage,
        output_format: outputFormat,
        speaker_diarization: speakerDiarization,
        max_line_length: maxLineLength
      };

      // Add multi-language support if languages are selected
      if (multiLanguages.length > 0) {
        requestBody.languages = multiLanguages;
      }

      const response = await api.request<{ job_id: string; status: string }>(
        "/api/v1/subtitles/generate",
        {
          method: "POST",
          body: JSON.stringify(requestBody)
        }
      );

      setJobId(response.job_id);
      setJobStatus(response.status);
      pollJobStatus(response.job_id);
    } catch (err: any) {
      setError(err.message || "Failed to start subtitle generation");
      setLoading(false);
    }
  };

  const handleTranslateSubtitles = async () => {
    if (!subtitleUrl.trim()) {
      setError("Please enter a subtitle URL");
      return;
    }
    
    if (targetLanguages.length === 0) {
      setError("Please select at least one target language");
      return;
    }

    setError(null);
    setLoading(true);
    setJobId(null);
    setJobStatus(null);
    setResult(null);

    try {
      const response = await api.request<{ job_id: string; status: string }>(
        "/api/v1/subtitles/translate",
        {
          method: "POST",
          body: JSON.stringify({
            subtitle_url: subtitleUrl,
            target_languages: targetLanguages,
            translation_service: translationService,
            preserve_timing: preserveTiming
          })
        }
      );

      setJobId(response.job_id);
      setJobStatus(response.status);
      pollJobStatus(response.job_id);
    } catch (err: any) {
      setError(err.message || "Failed to start subtitle translation");
      setLoading(false);
    }
  };

  const handleBurnSubtitles = async () => {
    if (!videoUrl.trim()) {
      setError("Please enter a video URL");
      return;
    }
    
    if (!burnSubtitleUrl.trim()) {
      setError("Please enter a subtitle URL");
      return;
    }

    setError(null);
    setLoading(true);
    setJobId(null);
    setJobStatus(null);
    setResult(null);

    try {
      const response = await api.request<{ job_id: string; status: string }>(
        "/api/v1/subtitles/burn",
        {
          method: "POST",
          body: JSON.stringify({
            video_url: videoUrl,
            subtitle_url: burnSubtitleUrl,
            font_name: fontName,
            font_size: fontSize,
            font_color: fontColor,
            background_color: backgroundColor,
            position: position
          })
        }
      );

      setJobId(response.job_id);
      setJobStatus(response.status);
      pollJobStatus(response.job_id);
    } catch (err: any) {
      setError(err.message || "Failed to start subtitle burning");
      setLoading(false);
    }
  };

  const pollJobStatus = async (id: string) => {
    const maxAttempts = 60;
    let attempts = 0;

    const checkStatus = async () => {
      try {
        const status = await api.request<{
          job_id: string;
          status: string;
          subtitle_urls?: Record<string, string>;
          video_url?: string;
          languages?: string[];
          processing_time?: number;
          error_message?: string;
        }>(`/api/v1/subtitles/status/${id}`);

        setJobStatus(status.status);

        if (status.status === "completed") {
          setResult({
            subtitle_urls: status.subtitle_urls,
            video_url: status.video_url,
            languages: status.languages,
            processing_time: status.processing_time
          });
          setLoading(false);
        } else if (status.status === "failed") {
          setError(status.error_message || "Operation failed");
          setLoading(false);
        } else if (attempts < maxAttempts) {
          attempts++;
          setTimeout(checkStatus, 5000);
        } else {
          setError("Job timeout - please check status manually");
          setLoading(false);
        }
      } catch (err: any) {
        setError(err.message || "Failed to check job status");
        setLoading(false);
      }
    };

    checkStatus();
  };

  const addTargetLanguage = () => {
    if (selectedLanguage && !targetLanguages.includes(selectedLanguage)) {
      setTargetLanguages([...targetLanguages, selectedLanguage]);
    }
  };

  const removeTargetLanguage = (lang: string) => {
    setTargetLanguages(targetLanguages.filter(l => l !== lang));
  };

  const addMultiLanguage = () => {
    if (selectedLanguage && !multiLanguages.includes(selectedLanguage)) {
      setMultiLanguages([...multiLanguages, selectedLanguage]);
    }
  };

  const removeMultiLanguage = (lang: string) => {
    setMultiLanguages(multiLanguages.filter(l => l !== lang));
  };

  return (
    <div className="container mx-auto py-8 px-4 max-w-6xl">
      <div className="mb-8">
        <h1 className="text-4xl font-bold mb-2">Subtitle Generator</h1>
        <p className="text-muted-foreground">
          Generate, translate, and burn subtitles with AI-powered ASR
        </p>
      </div>

      {error && (
        <div className="mb-6 p-4 bg-destructive/10 border border-destructive rounded-lg">
          <p className="text-destructive">{error}</p>
        </div>
      )}

      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="generate">
            <FileText className="mr-2 h-4 w-4" />
            Generate
          </TabsTrigger>
          <TabsTrigger value="translate">
            <Languages className="mr-2 h-4 w-4" />
            Translate
          </TabsTrigger>
          <TabsTrigger value="burn">
            <Video className="mr-2 h-4 w-4" />
            Burn
          </TabsTrigger>
        </TabsList>

        {/* Generate Subtitles Tab */}
        <TabsContent value="generate" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Generate Subtitles from Audio</CardTitle>
              <CardDescription>
                Use AI-powered ASR to generate subtitles from audio files
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <Label htmlFor="audio_url">Audio URL (S3)</Label>
                <Input
                  id="audio_url"
                  value={audioUrl}
                  onChange={(e) => setAudioUrl(e.target.value)}
                  placeholder="s3://bucket/path/to/audio.mp3"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="model_name">ASR Model</Label>
                  <Select value={modelName} onValueChange={setModelName}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="whisper-large-v3">Whisper Large V3</SelectItem>
                      <SelectItem value="whisper-medium">Whisper Medium</SelectItem>
                      <SelectItem value="whisper-small">Whisper Small</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div>
                  <Label htmlFor="source_language">Source Language</Label>
                  <Select value={sourceLanguage} onValueChange={setSourceLanguage}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      {supportedLanguages.map((lang) => (
                        <SelectItem key={lang} value={lang}>
                          {lang.toUpperCase()}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="output_format">Output Format</Label>
                  <Select value={outputFormat} onValueChange={setOutputFormat}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      {supportedFormats.map((format) => (
                        <SelectItem key={format} value={format}>
                          {format.toUpperCase()}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div>
                  <Label htmlFor="max_line_length">Max Line Length</Label>
                  <Input
                    id="max_line_length"
                    type="number"
                    min={20}
                    max={80}
                    value={maxLineLength}
                    onChange={(e) => setMaxLineLength(parseInt(e.target.value) || 42)}
                  />
                </div>
              </div>

              <div className="flex items-center space-x-2">
                <Checkbox
                  id="speaker_diarization"
                  checked={speakerDiarization}
                  onCheckedChange={(checked) => setSpeakerDiarization(checked === true)}
                />
                <Label htmlFor="speaker_diarization">Speaker Diarization</Label>
              </div>

              {/* Multi-language support */}
              <div>
                <Label>Generate in Multiple Languages (Optional)</Label>
                <div className="flex gap-2 mt-2">
                  <Select value={selectedLanguage} onValueChange={setSelectedLanguage}>
                    <SelectTrigger className="flex-1">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      {supportedLanguages.map((lang) => (
                        <SelectItem key={lang} value={lang}>
                          {lang.toUpperCase()}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                  <Button type="button" variant="outline" onClick={addMultiLanguage}>
                    Add
                  </Button>
                </div>
                {multiLanguages.length > 0 && (
                  <div className="flex flex-wrap gap-2 mt-2">
                    {multiLanguages.map((lang) => (
                      <Badge key={lang} variant="secondary" className="flex items-center gap-1">
                        {lang.toUpperCase()}
                        <button
                          onClick={() => removeMultiLanguage(lang)}
                          className="ml-1 hover:text-destructive"
                        >
                          ×
                        </button>
                      </Badge>
                    ))}
                  </div>
                )}
              </div>

              <Button
                onClick={handleGenerateSubtitles}
                disabled={loading}
                className="w-full"
              >
                {loading ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Generating...
                  </>
                ) : (
                  "Generate Subtitles"
                )}
              </Button>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Translate Subtitles Tab */}
        <TabsContent value="translate" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Translate Subtitles</CardTitle>
              <CardDescription>
                Translate existing subtitles to multiple languages
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <Label htmlFor="subtitle_url">Subtitle URL (S3)</Label>
                <Input
                  id="subtitle_url"
                  value={subtitleUrl}
                  onChange={(e) => setSubtitleUrl(e.target.value)}
                  placeholder="s3://bucket/path/to/subtitles.srt"
                />
              </div>

              <div>
                <Label htmlFor="translation_service">Translation Service</Label>
                <Select value={translationService} onValueChange={setTranslationService}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {translationServices.map((service) => (
                      <SelectItem key={service.service} value={service.service}>
                        {service.service} ({service.provider})
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div>
                <Label>Target Languages</Label>
                <div className="flex gap-2 mt-2">
                  <Select value={selectedLanguage} onValueChange={setSelectedLanguage}>
                    <SelectTrigger className="flex-1">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      {supportedLanguages.map((lang) => (
                        <SelectItem key={lang} value={lang}>
                          {lang.toUpperCase()}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                  <Button type="button" variant="outline" onClick={addTargetLanguage}>
                    Add
                  </Button>
                </div>
                {targetLanguages.length > 0 && (
                  <div className="flex flex-wrap gap-2 mt-2">
                    {targetLanguages.map((lang) => (
                      <Badge key={lang} variant="secondary" className="flex items-center gap-1">
                        {lang.toUpperCase()}
                        <button
                          onClick={() => removeTargetLanguage(lang)}
                          className="ml-1 hover:text-destructive"
                        >
                          ×
                        </button>
                      </Badge>
                    ))}
                  </div>
                )}
              </div>

              <div className="flex items-center space-x-2">
                <Checkbox
                  id="preserve_timing"
                  checked={preserveTiming}
                  onCheckedChange={(checked) => setPreserveTiming(checked === true)}
                />
                <Label htmlFor="preserve_timing">Preserve Original Timestamps</Label>
              </div>

              <Button
                onClick={handleTranslateSubtitles}
                disabled={loading}
                className="w-full"
              >
                {loading ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Translating...
                  </>
                ) : (
                  "Translate Subtitles"
                )}
              </Button>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Burn Subtitles Tab */}
        <TabsContent value="burn" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Burn Subtitles into Video</CardTitle>
              <CardDescription>
                Hardcode subtitles directly into video files
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <Label htmlFor="video_url">Video URL (S3)</Label>
                <Input
                  id="video_url"
                  value={videoUrl}
                  onChange={(e) => setVideoUrl(e.target.value)}
                  placeholder="s3://bucket/path/to/video.mp4"
                />
              </div>

              <div>
                <Label htmlFor="burn_subtitle_url">Subtitle URL (S3)</Label>
                <Input
                  id="burn_subtitle_url"
                  value={burnSubtitleUrl}
                  onChange={(e) => setBurnSubtitleUrl(e.target.value)}
                  placeholder="s3://bucket/path/to/subtitles.srt"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="font_name">Font Name</Label>
                  <Input
                    id="font_name"
                    value={fontName}
                    onChange={(e) => setFontName(e.target.value)}
                  />
                </div>

                <div>
                  <Label htmlFor="font_size">Font Size</Label>
                  <Input
                    id="font_size"
                    type="number"
                    min={12}
                    max={72}
                    value={fontSize}
                    onChange={(e) => setFontSize(parseInt(e.target.value) || 24)}
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="font_color">Font Color</Label>
                  <Input
                    id="font_color"
                    value={fontColor}
                    onChange={(e) => setFontColor(e.target.value)}
                    placeholder="white"
                  />
                </div>

                <div>
                  <Label htmlFor="background_color">Background Color</Label>
                  <Input
                    id="background_color"
                    value={backgroundColor}
                    onChange={(e) => setBackgroundColor(e.target.value)}
                    placeholder="black"
                  />
                </div>
              </div>

              <div>
                <Label htmlFor="position">Position</Label>
                <Select value={position} onValueChange={setPosition}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="top">Top</SelectItem>
                    <SelectItem value="bottom">Bottom</SelectItem>
                    <SelectItem value="center">Center</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <Button
                onClick={handleBurnSubtitles}
                disabled={loading}
                className="w-full"
              >
                {loading ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Burning...
                  </>
                ) : (
                  "Burn Subtitles"
                )}
              </Button>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      {/* Job Status */}
      {jobId && (
        <Card className="mt-6">
          <CardHeader>
            <CardTitle>Job Status</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center space-x-2">
              {jobStatus === "completed" && <CheckCircle2 className="h-5 w-5 text-green-500" />}
              {jobStatus === "failed" && <XCircle className="h-5 w-5 text-red-500" />}
              {jobStatus === "processing" && <Loader2 className="h-5 w-5 animate-spin" />}
              <Badge variant={jobStatus === "completed" ? "default" : jobStatus === "failed" ? "destructive" : "secondary"}>
                {jobStatus}
              </Badge>
            </div>
            
            {jobId && (
              <p className="text-sm text-muted-foreground">Job ID: {jobId}</p>
            )}

            {result && (
              <div className="space-y-2">
                {result.subtitle_urls && (
                  <div>
                    <Label>Subtitle URLs</Label>
                    {Object.entries(result.subtitle_urls).map(([lang, url]) => (
                      <div key={lang} className="text-sm font-mono break-all">
                        <strong>{lang.toUpperCase()}:</strong> {url as string}
                      </div>
                    ))}
                  </div>
                )}
                {result.video_url && (
                  <div>
                    <Label>Video URL</Label>
                    <p className="text-sm font-mono break-all">{result.video_url}</p>
                  </div>
                )}
                {result.languages && (
                  <div>
                    <Label>Languages</Label>
                    <p className="text-sm">{result.languages.join(", ")}</p>
                  </div>
                )}
                {result.processing_time && (
                  <div>
                    <Label>Processing Time</Label>
                    <p className="text-sm">{result.processing_time.toFixed(2)} seconds</p>
                  </div>
                )}
              </div>
            )}
          </CardContent>
        </Card>
      )}
    </div>
  );
}
