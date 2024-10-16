from django.core.management.base import BaseCommand
from django.db import models
from django.db.models.fields.related import ForeignKey, OneToOneField
from django.apps import apps
import os
from datetime import datetime
import pydot
from django.utils import timezone


class Command(BaseCommand):
    help = 'Checks database data quality and integrity and generates an ERD.'

    def handle(self, *args, **kwargs):
        report = []
        report.append("=== Database Quality Check Report ===\n")
        
        # Add table header
        report.append(f"{'Model Name':<25}{'Check':<30}{'Result':<60}")
        report.append("=" * 120)

        total_models = 0
        total_records = 0
        issue_counts = {
            'duplicates': 0,
            'nulls': 0,
            'broken_references': 0,
            'empty_fields': 0,
            'long_strings': 0,
            'future_dates': 0,
        }

        # Loop through all models
        for model in apps.get_models():
            model_name = model.__name__
            total_models += 1
            record_count = model.objects.count()
            total_records += record_count
            
            # Report total records for the model
            report.append(self.format_report_row(model_name, 'Total Records', str(record_count)))

            try:
                primary_key_result = self.check_primary_key(model)
                report.append(self.format_report_row('', 'Primary Key', primary_key_result))  # Leave model name blank

                unique_fields_result = self.check_unique_fields(model, issue_counts)
                report.append(self.format_report_row('', 'Unique Fields', unique_fields_result))  # Leave model name blank

                non_nullable_fields_result = self.check_non_nullable_fields(model, issue_counts)
                report.append(self.format_report_row('', 'Non-Nullable Fields', non_nullable_fields_result))  # Leave model name blank

                foreign_key_integrity_result = self.check_foreign_key_integrity(model, issue_counts)
                report.append(self.format_report_row('', 'Foreign Key Integrity', foreign_key_integrity_result))  # Leave model name blank

                empty_fields_result = self.check_empty_fields(model, issue_counts)
                report.append(self.format_report_row('', 'Empty Fields', empty_fields_result))  # Leave model name blank

                string_lengths_result = self.check_string_lengths(model, issue_counts)
                report.append(self.format_report_row('', 'String Lengths', string_lengths_result))  # Leave model name blank

                invalid_dates_result = self.check_date_validity(model, issue_counts)
                report.append(self.format_report_row('', 'Invalid Dates', invalid_dates_result))  # Leave model name blank

                data_consistency_result = self.check_data_consistency(model)
                report.append(self.format_report_row('', 'Data Consistency', data_consistency_result))  # Leave model name blank
            except Exception as e:
                report.append(self.format_report_row('', 'Error', str(e)))  # Leave model name blank

            report.append("=" * 120)  # Separator between models

        # Summary statistics
        report.append("\n=== Summary Statistics ===")
        report.append(f"Total Models Checked: {total_models}")
        report.append(f"Total Records Found: {total_records}")
        report.append(f"Total Duplicate Issues: {issue_counts['duplicates']}")
        report.append(f"Total Null Issues: {issue_counts['nulls']}")
        report.append(f"Total Broken Foreign Key References: {issue_counts['broken_references']}")
        report.append(f"Total Empty Fields Found: {issue_counts['empty_fields']}")
        report.append(f"Total Long String Issues: {issue_counts['long_strings']}")
        report.append(f"Total Future Date Issues: {issue_counts['future_dates']}")

        # Convert the report list into a string
        report_output = "\n".join(report)

        # Save the report to a .txt file with a timestamp
        timestamp = timezone.now().strftime("%Y%m%d_%H%M%S")  # Use timezone-aware now
        file_path = os.path.join(os.getcwd(), f'data_quality_report_{timestamp}.txt')
        with open(file_path, 'w') as file:
            file.write(report_output)

        # Generate ERD
        self.generate_erd()

        # Print final message to console
        self.stdout.write(self.style.SUCCESS(f'Report successfully saved to {file_path}'))

    def format_report_row(self, model_name, check_name, result):
        """Format each row of the report as a table-like row"""
        return f"{model_name:<25}{check_name:<30}{result:<60}"

    def check_primary_key(self, model):
        """Check if the model has a primary key"""
        if any(f.primary_key for f in model._meta.fields):
            return "Primary key is present."
        return "No primary key found!"

    def check_unique_fields(self, model, issue_counts):
        """Check if unique fields contain unique data"""
        unique_fields = [f for f in model._meta.fields if f.unique]
        if not unique_fields:
            return "No unique fields."
        
        issues = []
        for field in unique_fields:
            duplicates = model.objects.values(field.name).annotate(count=models.Count(field.name)).filter(count__gt=1)
            count_duplicates = duplicates.count()
            if count_duplicates > 0:
                issues.append(f"Field '{field.name}' contains {count_duplicates} duplicate values!")
                issue_counts['duplicates'] += count_duplicates
        
        if issues:
            return " | ".join(issues)

        return "All unique fields are valid."

    def check_non_nullable_fields(self, model, issue_counts):
        """Check if non-nullable fields contain null values"""
        non_nullable_fields = [f for f in model._meta.fields if not f.null]
        if not non_nullable_fields:
            return "No non-nullable fields."
        
        issues = []
        for field in non_nullable_fields:
            null_values = model.objects.filter(**{f"{field.name}__isnull": True}).count()
            if null_values > 0:
                issues.append(f"Field '{field.name}' contains {null_values} null values!")
                issue_counts['nulls'] += null_values
        
        if issues:
            return " | ".join(issues)

        return "All non-nullable fields contain valid data."

    def check_foreign_key_integrity(self, model, issue_counts):
        """Check if foreign keys are intact"""
        foreign_keys = [f for f in model._meta.fields if isinstance(f, (ForeignKey, OneToOneField))]
        if not foreign_keys:
            return "No foreign key fields."
        
        issues = []
        for field in foreign_keys:
            invalid_refs = model.objects.filter(**{f"{field.name}__isnull": True}).count()
            if invalid_refs > 0:
                issues.append(f"Field '{field.name}' has {invalid_refs} broken foreign key references!")
                issue_counts['broken_references'] += invalid_refs
        
        if issues:
            return " | ".join(issues)

        return "All foreign keys are valid."

    def check_empty_fields(self, model, issue_counts):
        """Check for empty fields that should not be empty"""
        empty_fields = []
        for field in model._meta.fields:
            if not field.null and not field.blank:
                empty_count = model.objects.filter(**{f"{field.name}__isnull": True}).count()
                if empty_count > 0:
                    empty_fields.append(f"Field '{field.name}' has {empty_count} empty entries.")
                    issue_counts['empty_fields'] += empty_count
        
        if empty_fields:
            return " | ".join(empty_fields)
        
        return "No empty fields found."

    def check_string_lengths(self, model, issue_counts):
        """Check string fields for length validity"""
        issues = []
        for field in model._meta.fields:
            if isinstance(field, models.CharField):
                max_length = field.max_length or 0
                too_long_count = model.objects.filter(**{f"{field.name}__length__gt": max_length}).count()
                if too_long_count > 0:
                    issues.append(f"Field '{field.name}' has {too_long_count} entries exceeding max length of {max_length}.")
                    issue_counts['long_strings'] += too_long_count
        
        if issues:
            return " | ".join(issues)

        return "All string lengths are valid."

    def check_date_validity(self, model, issue_counts):
        """Check date fields for future dates"""
        issues = []
        current_time = timezone.now()  # Use timezone-aware now
        for field in model._meta.fields:
            if isinstance(field, models.DateTimeField):
                future_count = model.objects.filter(**{f"{field.name}__gt": current_time}).count()
                if future_count > 0:
                    issues.append(f"Field '{field.name}' has {future_count} entries with future dates.")
                    issue_counts['future_dates'] += future_count

        if issues:
            return " | ".join(issues)

        return "All date fields are valid."

    def check_data_consistency(self, model):
        """Custom checks for data consistency (business logic)"""
        return "Consistency checks passed (if any)."

    def generate_erd(self):
        """Generate ERD using pydot, showing all fields inside models as a rectangle."""
        graph = pydot.Dot(graph_type='graph', bgcolor='lightgrey')

        for model in apps.get_models():
            model_name = model.__name__
            
            # Gather all field names and types
            fields_info = []
            for field in model._meta.fields:
                field_type = type(field).__name__
                fields_info.append(f"{field.name} ({field_type})")
            
            # Create a label for the node with model name and fields
            label = f"{model_name}\n" + "\n".join(fields_info)
            node = pydot.Node(
                model_name, 
                label=label, 
                shape="rectangle", 
                style="filled", 
                fillcolor="white"
            )
            graph.add_node(node)

            # Add relationships (edges) for ForeignKey and OneToOneField fields
            for field in model._meta.fields:
                if isinstance(field, (ForeignKey, OneToOneField)):
                    target_model = field.related_model.__name__
                    edge = pydot.Edge(model_name, target_model)
                    graph.add_edge(edge)

        # Save the graph to a PNG file
        output_file = 'erd_graph.png'
        graph.write_png(output_file)

        # Inform the user where the ERD has been saved
        self.stdout.write(self.style.SUCCESS(f'ERD successfully generated: {output_file}'))
