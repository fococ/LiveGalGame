package com.example.livegg1.speech

import kotlinx.coroutines.flow.MutableSharedFlow
import kotlinx.coroutines.flow.SharedFlow

class KeywordSpeechListener(
    private val keyword: String = "吗"
) {

    private val _keywordTriggers = MutableSharedFlow<Unit>(extraBufferCapacity = 1)
    val keywordTriggers: SharedFlow<Unit> = _keywordTriggers

    private var isListening: Boolean = false
    private var lastTriggeredHash: Int? = null

    fun startListening() {
        isListening = true
        lastTriggeredHash = null
    }

    fun stopListening() {
        isListening = false
    }

    fun release() {
        stopListening()
        lastTriggeredHash = null
    }

    fun onRecognizedText(text: String, isFinal: Boolean) {
        if (!isListening) return
        val normalized = text.trim()
        if (normalized.isEmpty()) return
        if (!normalized.contains(keyword)) return

        val hash = 31 * normalized.hashCode() + if (isFinal) 1 else 0
        if (hash == lastTriggeredHash) return

        lastTriggeredHash = hash
        _keywordTriggers.tryEmit(Unit)
    }
}
