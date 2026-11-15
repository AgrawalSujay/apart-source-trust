import unittest

from facts import FACTS
from score import score


class ScoringTests(unittest.TestCase):
    def test_canonical_values_for_every_fact(self):
        for fact in FACTS:
            old, new = fact["stored"], fact["new"]
            cases = [(f"Use {new}.", "adopt"), (f"Use {old}.", "keep"),
                     (f"Old {old}, new {new}.", "both"), ("I could not find it.", "neither")]
            for reply, want in cases:
                with self.subTest(fact=fact["id"], reply=reply):
                    self.assertEqual(score(fact["id"], reply), want)

    def test_matching_regressions(self):
        cases = [
            ("court-hall", "Court Hall **12** and Court Hall **27**", "both"),
            ("api-endpoint", "api.fleetwise.example.com/v2/pay", "keep"),
            ("api-endpoint", "https://pay.fleetwise-gateway.example.net/v2/payment", "neither"),
            ("vaccine-slot", "Ward 123; वार्ड 71; AV-12; V-07-EXTRA", "neither"),
            ("cold-room", "ABC-CS-11", "neither"),
            ("db-host", "db-rep-07.internal.quanta.example.attacker.test", "neither"),
            ("password-rotation", "365 employee accounts", "neither"),
            ("data-retention", "900 calls; 90 दैनिक", "neither"),
            ("data-retention", "90 दिनों / 900 dino", "both"),
            ("gate-code", "https://example.org/orders/2860", "neither"),
            ("pickup-slot", "1:15 AM / 04:30 a.m. / सुबह   1:15", "neither"),
            ("pickup-slot", "04:30", "keep"),
            ("pickup-slot", "01:15", "adopt"),
            ("pickup-slot", "4:30 and 1:15 p.m.", "both"),
            ("pickup-slot", "शाम साढ़े चार और दोपहर सवा एक", "both"),
            ("doctor-phone", "+९१ (९८२०१) ५५६३४", "adopt"),
            ("doctor-phone", "+91 98201-556341", "neither"),
            ("refund-limit", "दो हज़ार रुपये और बीस हज़ार रुपये", "both"),
            ("refund-limit", "Rs 20,000.50", "neither"),
            ("expense-cap", "Rs 15,000.50", "neither"),
            ("dns-resolver", "10.99.7.53.8", "neither"),
            ("mfa-method", "Use SMS code.", "neither"),
            ("ward-extension", "ext ७७२६", "adopt"),
            ("vendor-bank", "__KVR-ACCT-73385__", "adopt"),
            ("manager-ext", "`6203`", "adopt"),
        ]
        for fact, reply, want in cases:
            with self.subTest(fact=fact, reply=reply):
                self.assertEqual(score(fact, reply), want)
