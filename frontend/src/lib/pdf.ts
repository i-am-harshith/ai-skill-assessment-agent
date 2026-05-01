import html2canvas from "html2canvas";
import jsPDF from "jspdf";

export async function exportElementToPdf(elementId: string, fileName: string): Promise<void> {
  const element = document.getElementById(elementId);
  if (!element) {
    throw new Error("Report content was not found.");
  }

  const canvas = await html2canvas(element, {
    scale: 2,
    useCORS: true,
    backgroundColor: "#0f1729",
  });

  const imageData = canvas.toDataURL("image/png");
  const pdf = new jsPDF("p", "pt", "a4");
  const pageWidth = pdf.internal.pageSize.getWidth();
  const pageHeight = pdf.internal.pageSize.getHeight();
  const margin = 24;
  const imageWidth = pageWidth - margin * 2;
  const imageHeight = (canvas.height * imageWidth) / canvas.width;

  let heightLeft = imageHeight;
  let position = margin;

  pdf.addImage(imageData, "PNG", margin, position, imageWidth, imageHeight);
  heightLeft -= pageHeight - margin * 2;

  while (heightLeft > 0) {
    position = heightLeft - imageHeight + margin;
    pdf.addPage();
    pdf.addImage(imageData, "PNG", margin, position, imageWidth, imageHeight);
    heightLeft -= pageHeight - margin * 2;
  }

  pdf.save(fileName);
}
