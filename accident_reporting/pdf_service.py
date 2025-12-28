"""
事故・ヒヤリハット報告書のPDF生成サービス

厚生労働省の標準様式に準拠したPDF帳票を生成します。
行政提出に耐える体裁で、印刷前提のレイアウトを採用しています。
"""
import io
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import os


# 日本語フォントの登録（システムにインストールされているフォントを使用）
FONT_PATH = '/usr/share/fonts/truetype/fonts-japanese-gothic.ttf'
FONT_PATH_ALT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
FONT_PATH_ALT2 = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'

def register_japanese_font():
    """日本語フォントを登録する"""
    try:
        if os.path.exists(FONT_PATH):
            pdfmetrics.registerFont(TTFont('Japanese', FONT_PATH))
            return 'Japanese'
        elif os.path.exists(FONT_PATH_ALT):
            pdfmetrics.registerFont(TTFont('Japanese', FONT_PATH_ALT))
            return 'Japanese'
        elif os.path.exists(FONT_PATH_ALT2):
            pdfmetrics.registerFont(TTFont('Japanese', FONT_PATH_ALT2))
            return 'Japanese'
        else:
            # フォントが見つからない場合はデフォルトを使用
            return 'Helvetica'
    except Exception:
        return 'Helvetica'


def generate_accident_report_pdf(report) -> bytes:
    """
    事故報告書のPDFを生成する
    
    Args:
        report: AccidentReportモデルのインスタンス
    
    Returns:
        bytes: 生成されたPDFのバイナリデータ
    """
    buffer = io.BytesIO()
    
    # フォント登録
    font_name = register_japanese_font()
    
    # ドキュメント設定
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=15*mm,
        leftMargin=15*mm,
        topMargin=15*mm,
        bottomMargin=15*mm
    )
    
    # スタイル定義
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontName=font_name,
        fontSize=16,
        alignment=TA_CENTER,
        spaceAfter=10*mm
    )
    
    header_style = ParagraphStyle(
        'Header',
        parent=styles['Normal'],
        fontName=font_name,
        fontSize=10,
        alignment=TA_LEFT
    )
    
    normal_style = ParagraphStyle(
        'Normal',
        parent=styles['Normal'],
        fontName=font_name,
        fontSize=9,
        alignment=TA_LEFT,
        leading=12
    )
    
    small_style = ParagraphStyle(
        'Small',
        parent=styles['Normal'],
        fontName=font_name,
        fontSize=8,
        alignment=TA_LEFT
    )
    
    # コンテンツ構築
    elements = []
    
    # タイトル
    report_type_text = "事故報告書" if report.report_type == 'accident' else "ヒヤリハット報告書"
    elements.append(Paragraph(report_type_text, title_style))
    
    # 基本情報テーブル
    basic_info_data = [
        ['報告日', datetime.now().strftime('%Y年%m月%d日'), '報告者', report.reporter.username if report.reporter else ''],
        ['発生日時', report.occurred_at.strftime('%Y年%m月%d日 %H時%M分') if report.occurred_at else '', '発生場所', report.location_detail or ''],
        ['事業所名', report.location.name if report.location else '', 'サービス種別', report.get_service_type_display() if report.service_type else ''],
        ['利用者名', report.client.full_name if report.client else '', '利用者ID', str(report.client.id) if report.client else ''],
    ]
    
    basic_info_table = Table(basic_info_data, colWidths=[25*mm, 55*mm, 25*mm, 55*mm])
    basic_info_table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), font_name, 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('BACKGROUND', (2, 0), (2, -1), colors.lightgrey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        ('ALIGN', (2, 0), (2, -1), 'CENTER'),
        ('LEFTPADDING', (0, 0), (-1, -1), 3*mm),
        ('RIGHTPADDING', (0, 0), (-1, -1), 3*mm),
        ('TOPPADDING', (0, 0), (-1, -1), 2*mm),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2*mm),
    ]))
    elements.append(basic_info_table)
    elements.append(Spacer(1, 5*mm))
    
    # 事故の状況
    elements.append(Paragraph("【事故の状況】", header_style))
    overview_text = report.ai_generated_overview or report.incident_description or '（記載なし）'
    overview_data = [[Paragraph(overview_text, normal_style)]]
    overview_table = Table(overview_data, colWidths=[160*mm])
    overview_table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), font_name, 9),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
        ('LEFTPADDING', (0, 0), (-1, -1), 3*mm),
        ('RIGHTPADDING', (0, 0), (-1, -1), 3*mm),
        ('TOPPADDING', (0, 0), (-1, -1), 2*mm),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2*mm),
    ]))
    elements.append(overview_table)
    elements.append(Spacer(1, 5*mm))
    
    # 被害の状況
    elements.append(Paragraph("【被害の状況】", header_style))
    damage_text = report.damage_status or '（記載なし）'
    damage_data = [[Paragraph(damage_text, normal_style)]]
    damage_table = Table(damage_data, colWidths=[160*mm])
    damage_table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), font_name, 9),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
        ('LEFTPADDING', (0, 0), (-1, -1), 3*mm),
        ('RIGHTPADDING', (0, 0), (-1, -1), 3*mm),
        ('TOPPADDING', (0, 0), (-1, -1), 2*mm),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2*mm),
    ]))
    elements.append(damage_table)
    elements.append(Spacer(1, 5*mm))
    
    # 初期対応
    elements.append(Paragraph("【初期対応】", header_style))
    response_text = report.initial_response or '（記載なし）'
    response_data = [[Paragraph(response_text, normal_style)]]
    response_table = Table(response_data, colWidths=[160*mm])
    response_table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), font_name, 9),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
        ('LEFTPADDING', (0, 0), (-1, -1), 3*mm),
        ('RIGHTPADDING', (0, 0), (-1, -1), 3*mm),
        ('TOPPADDING', (0, 0), (-1, -1), 2*mm),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2*mm),
    ]))
    elements.append(response_table)
    elements.append(Spacer(1, 5*mm))
    
    # 原因分析
    elements.append(Paragraph("【原因分析】", header_style))
    cause_text = report.ai_generated_cause_analysis or '（記載なし）'
    cause_data = [[Paragraph(cause_text, normal_style)]]
    cause_table = Table(cause_data, colWidths=[160*mm])
    cause_table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), font_name, 9),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
        ('LEFTPADDING', (0, 0), (-1, -1), 3*mm),
        ('RIGHTPADDING', (0, 0), (-1, -1), 3*mm),
        ('TOPPADDING', (0, 0), (-1, -1), 2*mm),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2*mm),
    ]))
    elements.append(cause_table)
    elements.append(Spacer(1, 5*mm))
    
    # 再発防止策
    elements.append(Paragraph("【再発防止策】", header_style))
    prevention_text = report.ai_generated_prevention_plan or '（記載なし）'
    prevention_data = [[Paragraph(prevention_text, normal_style)]]
    prevention_table = Table(prevention_data, colWidths=[160*mm])
    prevention_table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), font_name, 9),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
        ('LEFTPADDING', (0, 0), (-1, -1), 3*mm),
        ('RIGHTPADDING', (0, 0), (-1, -1), 3*mm),
        ('TOPPADDING', (0, 0), (-1, -1), 2*mm),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2*mm),
    ]))
    elements.append(prevention_table)
    elements.append(Spacer(1, 5*mm))
    
    # 行政報告要否
    gov_report_text = "要" if report.is_government_report_needed else "不要"
    gov_reason_text = report.government_report_reason or '（判定理由なし）'
    elements.append(Paragraph(f"【行政報告要否】 {gov_report_text}", header_style))
    elements.append(Paragraph(f"判定理由: {gov_reason_text}", small_style))
    elements.append(Spacer(1, 10*mm))
    
    # 署名欄
    signature_data = [
        ['管理者確認', '', '確認日', ''],
        ['署名', '', '', ''],
    ]
    signature_table = Table(signature_data, colWidths=[25*mm, 55*mm, 25*mm, 55*mm])
    signature_table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), font_name, 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('BACKGROUND', (2, 0), (2, -1), colors.lightgrey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        ('ALIGN', (2, 0), (2, -1), 'CENTER'),
        ('LEFTPADDING', (0, 0), (-1, -1), 3*mm),
        ('RIGHTPADDING', (0, 0), (-1, -1), 3*mm),
        ('TOPPADDING', (0, 0), (-1, -1), 4*mm),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4*mm),
    ]))
    elements.append(signature_table)
    
    # フッター（注意書き）
    elements.append(Spacer(1, 5*mm))
    footer_text = "※本報告書は電子的に作成・保存されています。印刷日時: " + datetime.now().strftime('%Y年%m月%d日 %H:%M')
    elements.append(Paragraph(footer_text, small_style))
    
    # PDF生成
    doc.build(elements)
    
    buffer.seek(0)
    return buffer.getvalue()
