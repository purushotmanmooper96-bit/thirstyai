let
    Source = Csv.Document(File.Contents(ProjectRoot & "\data\processed\india_groundwater_2025.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    Types = Table.TransformColumnTypes(Headers, {{"state", type text}, {"recharge_bcm", type number}, {"extractable_bcm", type number}, {"extraction_bcm", type number}, {"stage_pct", type number}, {"year", Int64.Type}, {"source_id", type text}})
in
    Types
