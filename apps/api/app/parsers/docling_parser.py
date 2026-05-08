from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator

from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import (
    PdfPipelineOptions,
    TableFormerMode,
)
from docling.document_converter import (
    DocumentConverter,
    PdfFormatOption,
)
from docling_core.types.doc import DoclingDocument

logger = logging.getLogger(__name__)


@dataclass
class ParseConfig:
    """Controls what Docling extracts. Tune this per use case."""

    do_ocr: bool = False              # Enable for scanned/image-based PDFs
    do_table_structure: bool = True   # Reconstruct table rows/cols/headers
    table_mode: TableFormerMode = TableFormerMode.ACCURATE  # or FAST
    generate_images: bool = False     # Extract embedded images
    images_scale: float = 2.0        # Resolution multiplier when images enabled


@dataclass
class ParseResult:
    file_path: Path
    document: DoclingDocument
    error: str | None = None

    @property
    def success(self) -> bool:
        return self.error is None

    def to_markdown(self) -> str:
        return self.document.export_to_markdown()

    def to_json(self) -> str:
        """Lossless export — preserves bounding boxes, page refs, element types."""
        return self.document.export_to_dict()

    def iter_tables(self) -> Iterator:
        """Yields tables as pandas DataFrames (requires docling[pandas])."""
        for table in self.document.tables:
            yield table.export_to_dataframe()


class DoclingParser:
    """
    Lazy-initialized Docling parser with explicit pipeline configuration.

    Usage:
        parser = DoclingParser()                        # default config
        parser = DoclingParser(ParseConfig(do_ocr=True)) # scanned PDFs

        result = parser.parse("report.pdf")
        results = list(parser.parse_many(["a.pdf", "b.pdf"]))
    """

    def __init__(self, config: ParseConfig | None = None):
        self.config = config or ParseConfig()
        self._converter: DocumentConverter | None = None  # lazy init

    @property
    def converter(self) -> DocumentConverter:
        """Initialize converter on first use, not at import time."""
        if self._converter is None:
            self._converter = self._build_converter()
        return self._converter

    def _build_converter(self) -> DocumentConverter:
        opts = PdfPipelineOptions(
            do_ocr=self.config.do_ocr,
            do_table_structure=self.config.do_table_structure,
            # table_structure_options={"mode": self.config.table_mode,},
            generate_picture_images=self.config.generate_images,
            images_scale=self.config.images_scale,
        )
        return DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(pipeline_options=opts)
            }
        )

    def parse(self, file_path: str | Path) -> ParseResult:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        if not path.is_file():
            raise ValueError(f"Path is not a file: {path}")

        try:
            result = self.converter.convert(str(path))
            return ParseResult(file_path=path, document=result.document)
        except Exception as e:
            logger.error("Failed to parse %s: %s", path, e)
            return ParseResult(file_path=path, document=None, error=str(e))

    def parse_many(
        self,
        file_paths: list[str | Path],
        *,
        raise_on_error: bool = False,
    ) -> Iterator[ParseResult]:
        """
        Batch conversion — faster than calling parse() in a loop.
        Docling parallelizes convert_all() internally.
        """
        paths = [Path(p) for p in file_paths]
        missing = [p for p in paths if not p.exists()]
        if missing:
            raise FileNotFoundError(f"Files not found: {missing}")

        for conv_result in self.converter.convert_all(
            [str(p) for p in paths]
        ):
            src = Path(conv_result.input.file)
            if conv_result.document is None:
                err = "Conversion returned no document"
                logger.error("Failed: %s — %s", src, err)
                if raise_on_error:
                    raise RuntimeError(f"{src}: {err}")
                yield ParseResult(file_path=src, document=None, error=err)
            else:
                yield ParseResult(file_path=src, document=conv_result.document)