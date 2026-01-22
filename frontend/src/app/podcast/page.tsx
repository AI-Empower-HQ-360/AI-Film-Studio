"use client";

/**
 * @label Podcast Mode Page
 * @description Next.js page for creating podcast-style videos with multiple characters
 */

import { useState, useEffect } from "react";
import { api } from "@/lib/api";
// Note: UI components should be created or imported from your component library
// For now, using basic HTML elements with Tailwind classes
// You may need to create these components or install shadcn/ui
import { Loader2, Play, CheckCircle2, XCircle, RefreshCw } from "lucide-react";

interface Character {
  character_id: string;
  image_url: string;
  voice_id: string;
  name: string;
  role: string;
}

interface DialogueLine {
  character_id: string;
  text: string;
  emotion: string;
  timestamp?: number;
}

interface PodcastLayout {
  layout: string;
  name: string;
  description: string;
  max_characters: number;
}

export default function PodcastModePage() {
  const [title, setTitle] = useState("");
  const [characters, setCharacters] = useState<Character[]>([
    { character_id: "char_1", image_url: "", voice_id: "", name: "", role: "Host" },
    { character_id: "char_2", image_url: "", voice_id: "", name: "", role: "Guest" }
  ]);
  const [dialogue, setDialogue] = useState<DialogueLine[]>([]);
  const [layout, setLayout] = useState("split_screen_50_50");
  const [backgroundStyle, setBackgroundStyle] = useState("studio");
  const [addLowerThirds, setAddLowerThirds] = useState(true);
  const [addBackgroundMusic, setAddBackgroundMusic] = useState(false);
  const [duration, setDuration] = useState<number | undefined>(undefined);
  
  const [layouts, setLayouts] = useState<PodcastLayout[]>([]);
  const [loadingLayouts, setLoadingLayouts] = useState(false);
  const [generating, setGenerating] = useState(false);
  const [jobId, setJobId] = useState<string | null>(null);
  const [jobStatus, setJobStatus] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<{
    video_url?: string;
    thumbnail_url?: string;
    duration?: number;
  } | null>(null);

  // Load layouts on mount
  useEffect(() => {
    loadLayouts();
  }, []);

  const loadLayouts = async () => {
    setLoadingLayouts(true);
    try {
      const response = await api.request<{ layouts: PodcastLayout[] }>("/api/v1/podcast/layouts");
      setLayouts(response.layouts || []);
    } catch (err) {
      console.error("Failed to load layouts:", err);
    } finally {
      setLoadingLayouts(false);
    }
  };

  const addCharacter = () => {
    if (characters.length < 4) {
      setCharacters([
        ...characters,
        {
          character_id: `char_${characters.length + 1}`,
          image_url: "",
          voice_id: "",
          name: "",
          role: "Speaker"
        }
      ]);
    }
  };

  const removeCharacter = (index: number) => {
    if (characters.length > 2) {
      setCharacters(characters.filter((_, i) => i !== index));
    }
  };

  const updateCharacter = (index: number, field: keyof Character, value: string) => {
    const updated = [...characters];
    updated[index] = { ...updated[index], [field]: value };
    setCharacters(updated);
  };

  const addDialogueLine = () => {
    if (characters.length > 0) {
      setDialogue([
        ...dialogue,
        {
          character_id: characters[0].character_id,
          text: "",
          emotion: "neutral"
        }
      ]);
    }
  };

  const updateDialogueLine = (index: number, field: keyof DialogueLine, value: string | number) => {
    const updated = [...dialogue];
    updated[index] = { ...updated[index], [field]: value };
    setDialogue(updated);
  };

  const removeDialogueLine = (index: number) => {
    setDialogue(dialogue.filter((_, i) => i !== index));
  };

  const handleGenerate = async () => {
    // Validation
    if (!title.trim()) {
      setError("Please enter a podcast title");
      return;
    }
    
    if (characters.some(c => !c.name || !c.image_url || !c.voice_id)) {
      setError("Please fill in all character fields (name, image URL, voice ID)");
      return;
    }
    
    if (dialogue.length === 0) {
      setError("Please add at least one dialogue line");
      return;
    }
    
    if (dialogue.some(d => !d.text.trim())) {
      setError("Please fill in all dialogue text");
      return;
    }

    setError(null);
    setGenerating(true);
    setJobId(null);
    setJobStatus(null);
    setResult(null);

    try {
      const response = await api.request<{ job_id: string; status: string }>(
        "/api/v1/podcast/generate",
        {
          method: "POST",
          body: JSON.stringify({
            title,
            characters,
            dialogue,
            layout,
            background_style: backgroundStyle,
            add_lower_thirds: addLowerThirds,
            add_background_music: addBackgroundMusic,
            duration: duration || undefined
          })
        }
      );

      setJobId(response.job_id);
      setJobStatus(response.status);
      
      // Start polling for status
      pollJobStatus(response.job_id);
    } catch (err: any) {
      setError(err.message || "Failed to start podcast generation");
      setGenerating(false);
    }
  };

  const pollJobStatus = async (id: string) => {
    const maxAttempts = 60; // 5 minutes max
    let attempts = 0;

    const checkStatus = async () => {
      try {
        const status = await api.request<{
          job_id: string;
          status: string;
          video_url?: string;
          thumbnail_url?: string;
          duration?: number;
          error_message?: string;
        }>(`/api/v1/podcast/status/${id}`);

        setJobStatus(status.status);

        if (status.status === "completed") {
          setResult({
            video_url: status.video_url,
            thumbnail_url: status.thumbnail_url,
            duration: status.duration
          });
          setGenerating(false);
        } else if (status.status === "failed") {
          setError(status.error_message || "Podcast generation failed");
          setGenerating(false);
        } else if (attempts < maxAttempts) {
          attempts++;
          setTimeout(checkStatus, 5000); // Check every 5 seconds
        } else {
          setError("Job timeout - please check status manually");
          setGenerating(false);
        }
      } catch (err: any) {
        setError(err.message || "Failed to check job status");
        setGenerating(false);
      }
    };

    checkStatus();
  };

  return (
    <div className="container mx-auto py-8 px-4 max-w-6xl">
      <div className="mb-8">
        <h1 className="text-4xl font-bold mb-2">Podcast Mode</h1>
        <p className="text-muted-foreground">
          Create podcast-style videos with multiple characters in conversation
        </p>
      </div>

      {error && (
        <div className="mb-6 p-4 bg-destructive/10 border border-destructive rounded-lg">
          <p className="text-destructive">{error}</p>
        </div>
      )}

      <div className="grid gap-6 md:grid-cols-2">
        {/* Left Column - Configuration */}
        <div className="space-y-6">
          {/* Basic Info */}
          <Card>
            <CardHeader>
              <CardTitle>Podcast Information</CardTitle>
              <CardDescription>Basic details for your podcast episode</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <Label htmlFor="title">Episode Title</Label>
                <Input
                  id="title"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  placeholder="My Podcast Episode"
                />
              </div>
              
              <div>
                <Label htmlFor="layout">Video Layout</Label>
                <Select value={layout} onValueChange={setLayout}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {loadingLayouts ? (
                      <SelectItem value="loading" disabled>Loading...</SelectItem>
                    ) : (
                      layouts.map((l) => (
                        <SelectItem key={l.layout} value={l.layout}>
                          {l.name} - {l.description}
                        </SelectItem>
                      ))
                    )}
                  </SelectContent>
                </Select>
              </div>

              <div>
                <Label htmlFor="background">Background Style</Label>
                <Select value={backgroundStyle} onValueChange={setBackgroundStyle}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="studio">Studio</SelectItem>
                    <SelectItem value="room">Room</SelectItem>
                    <SelectItem value="outdoor">Outdoor</SelectItem>
                    <SelectItem value="minimal">Minimal</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div>
                <Label htmlFor="duration">Duration (seconds, optional)</Label>
                <Input
                  id="duration"
                  type="number"
                  value={duration || ""}
                  onChange={(e) => setDuration(e.target.value ? parseInt(e.target.value) : undefined)}
                  placeholder="120"
                />
              </div>

              <div className="flex items-center space-x-2">
                <Checkbox
                  id="lower_thirds"
                  checked={addLowerThirds}
                  onCheckedChange={(checked) => setAddLowerThirds(checked === true)}
                />
                <Label htmlFor="lower_thirds">Add Lower Thirds (character names)</Label>
              </div>

              <div className="flex items-center space-x-2">
                <Checkbox
                  id="background_music"
                  checked={addBackgroundMusic}
                  onCheckedChange={(checked) => setAddBackgroundMusic(checked === true)}
                />
                <Label htmlFor="background_music">Add Background Music</Label>
              </div>
            </CardContent>
          </Card>

          {/* Characters */}
          <Card>
            <CardHeader>
              <CardTitle>Characters ({characters.length}/4)</CardTitle>
              <CardDescription>Configure characters for the podcast</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {characters.map((char, index) => (
                <div key={index} className="p-4 border rounded-lg space-y-3">
                  <div className="flex justify-between items-center">
                    <Label>Character {index + 1}</Label>
                    {characters.length > 2 && (
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => removeCharacter(index)}
                      >
                        Remove
                      </Button>
                    )}
                  </div>
                  
                  <div>
                    <Label>Name</Label>
                    <Input
                      value={char.name}
                      onChange={(e) => updateCharacter(index, "name", e.target.value)}
                      placeholder="Character name"
                    />
                  </div>
                  
                  <div>
                    <Label>Image URL (S3)</Label>
                    <Input
                      value={char.image_url}
                      onChange={(e) => updateCharacter(index, "image_url", e.target.value)}
                      placeholder="s3://bucket/path/to/image.jpg"
                    />
                  </div>
                  
                  <div>
                    <Label>Voice ID</Label>
                    <Input
                      value={char.voice_id}
                      onChange={(e) => updateCharacter(index, "voice_id", e.target.value)}
                      placeholder="voice_001"
                    />
                  </div>
                  
                  <div>
                    <Label>Role</Label>
                    <Select
                      value={char.role}
                      onValueChange={(value) => updateCharacter(index, "role", value)}
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="Host">Host</SelectItem>
                        <SelectItem value="Guest">Guest</SelectItem>
                        <SelectItem value="Speaker">Speaker</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>
              ))}
              
              {characters.length < 4 && (
                <Button variant="outline" onClick={addCharacter}>
                  Add Character
                </Button>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Right Column - Dialogue */}
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Dialogue</CardTitle>
              <CardDescription>Add conversation lines for your podcast</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {dialogue.map((line, index) => (
                <div key={index} className="p-4 border rounded-lg space-y-3">
                  <div className="flex justify-between items-center">
                    <Label>Line {index + 1}</Label>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => removeDialogueLine(index)}
                    >
                      Remove
                    </Button>
                  </div>
                  
                  <div>
                    <Label>Character</Label>
                    <Select
                      value={line.character_id}
                      onValueChange={(value) => updateDialogueLine(index, "character_id", value)}
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        {characters.map((char) => (
                          <SelectItem key={char.character_id} value={char.character_id}>
                            {char.name || `Character ${char.character_id}`}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                  
                  <div>
                    <Label>Text</Label>
                    <Textarea
                      value={line.text}
                      onChange={(e) => updateDialogueLine(index, "text", e.target.value)}
                      placeholder="Enter dialogue text..."
                      rows={3}
                    />
                  </div>
                  
                  <div>
                    <Label>Emotion</Label>
                    <Select
                      value={line.emotion}
                      onValueChange={(value) => updateDialogueLine(index, "emotion", value)}
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="neutral">Neutral</SelectItem>
                        <SelectItem value="happy">Happy</SelectItem>
                        <SelectItem value="sad">Sad</SelectItem>
                        <SelectItem value="excited">Excited</SelectItem>
                        <SelectItem value="serious">Serious</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>
              ))}
              
              <Button variant="outline" onClick={addDialogueLine}>
                Add Dialogue Line
              </Button>
            </CardContent>
          </Card>

          {/* Generate Button */}
          <Card>
            <CardContent className="pt-6">
              <Button
                onClick={handleGenerate}
                disabled={generating}
                className="w-full"
                size="lg"
              >
                {generating ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Generating Podcast...
                  </>
                ) : (
                  <>
                    <Play className="mr-2 h-4 w-4" />
                    Generate Podcast Video
                  </>
                )}
              </Button>
            </CardContent>
          </Card>

          {/* Job Status */}
          {jobId && (
            <Card>
              <CardHeader>
                <CardTitle>Generation Status</CardTitle>
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
                    {result.video_url && (
                      <div>
                        <Label>Video URL</Label>
                        <p className="text-sm font-mono break-all">{result.video_url}</p>
                      </div>
                    )}
                    {result.thumbnail_url && (
                      <div>
                        <Label>Thumbnail URL</Label>
                        <p className="text-sm font-mono break-all">{result.thumbnail_url}</p>
                      </div>
                    )}
                    {result.duration && (
                      <div>
                        <Label>Duration</Label>
                        <p className="text-sm">{result.duration} seconds</p>
                      </div>
                    )}
                  </div>
                )}
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
}
