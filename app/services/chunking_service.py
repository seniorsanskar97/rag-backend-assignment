from typing import List


class ChunkingService:
    def fixed_size_chunking(
        self,
        text: str,
        chunk_size: int = 500,
        overlap: int = 100,
    ) -> List[str]:
        chunks = []

        start = 0

        while start < len(text):
            end = start + chunk_size
            chunks.append(text[start:end])

            start += chunk_size - overlap

        return chunks

    def paragraph_chunking(self, text: str) -> List[str]:
        paragraphs = text.split("\n\n")

        return [
            paragraph.strip()
            for paragraph in paragraphs
            if paragraph.strip()
        ]