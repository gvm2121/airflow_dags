from dags.fecha import dia
from playwright.sync_api import sync_playwright, expect
from pathlib import Path
import time


def run():
    DESTINO = Path("rentabilidades.xlsx")
    with sync_playwright() as p:
        # 1. Lanzar Firefox
        browser = p.firefox.launch(headless=True)   # headless=False si quieres ver la UI
        page = browser.new_page()

        # 2. Navegar al formulario
        page.goto("https://estadisticas2.aafm.cl/")
        page.click("#CompleteListTabButton")

        date_input = page.locator("#Date")
        date_input.wait_for(state="visible")
        date_input.fill(dia) # YYYY-mm-dd
        #expect(date_input).to_have_value("2025-06-10")

        sel_cat_afm = page.locator('select[name="ListIdCategoryAafm"]')
        sel_cat_afm.select_option('0')
        expect(sel_cat_afm).to_have_values(['0'])

        sel_list_adm = page.locator('select[name="ListIdAdministrator"]')
        sel_list_adm.select_option('0')
        expect(sel_list_adm).to_have_values(['0'])

        sel_tipo_inv = page.locator('select[name="InversionType"]')
        sel_tipo_inv.select_option('A')
        expect(sel_tipo_inv).to_have_value('A')

        sel_tipo_apv = page.locator('#ApvRentability')
        sel_tipo_apv.select_option("3")
        expect(sel_tipo_apv).to_have_value("3")

        page.check('#PeriodAll')
        page.check('#RentRealSelected')

        page.get_by_role("button", name="Consultar").click()

        page.locator("#datatablesSimple3 tbody tr").first.wait_for(
            state="visible", timeout=60_000
        )
        excel_btn = page.locator("button.btn-excel:visible")
        excel_btn.wait_for(state="visible")
        with page.expect_download() as dl_info:
            excel_btn.click()    # <- botón exportar Excel
        download = dl_info.value                        # playwright.sync_api.Download
        download.save_as(DESTINO)                       # guarda en disco

        print(f"✅ Archivo descargado como '{DESTINO.resolve()}'")
        time.sleep(5)
        
if __name__ == "__main__":
    print("********* calculando************",dia)
    run()